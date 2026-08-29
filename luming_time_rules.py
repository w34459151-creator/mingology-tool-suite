"""禄命排盘的出生时间规则，独立于现有排盘流程。"""
from datetime import datetime, timedelta
import math
import json
from pathlib import Path


CHINA_PROVINCE_PREFIXES = (
    '中国', '中國', '北京', '天津', '河北', '山西', '内蒙古', '內蒙古',
    '辽宁', '遼寧', '吉林', '黑龙江', '黑龍江', '上海', '江苏', '江蘇',
    '浙江', '安徽', '福建', '江西', '山东', '山東', '河南', '湖北',
    '湖南', '广东', '廣東', '广西', '廣西', '海南', '重庆', '重慶',
    '四川', '贵州', '貴州', '云南', '雲南', '西藏', '陕西', '陝西',
    '甘肃', '甘肅', '青海', '宁夏', '寧夏', '新疆', '香港', '澳门',
    '澳門', '台湾', '臺灣',
)


def parse_time_text(text):
    """Parse H, H:M, or H:M:S and return datetime precision metadata."""
    raw = (text or '').strip()
    if not raw:
        raise ValueError('time is required')
    parts = raw.split(':')
    if len(parts) > 3:
        raise ValueError('invalid time')
    try:
        hour = int(parts[0])
        minute = int(parts[1]) if len(parts) > 1 and parts[1] else 0
        second = int(parts[2]) if len(parts) > 2 and parts[2] else 0
    except ValueError as exc:
        raise ValueError('invalid time') from exc
    if not 0 <= hour <= 23 or not 0 <= minute <= 59 or not 0 <= second <= 59:
        raise ValueError('invalid time')
    precision = 'second' if len(parts) == 3 else 'minute' if len(parts) == 2 else 'hour'
    return hour, minute, second, precision


def is_china_birthplace(text):
    normalized = ''.join(str(text or '').split())
    return normalized.startswith(CHINA_PROVINCE_PREFIXES)


def is_china_summer_time(local_dt, birthplace):
    """China mainland historical DST: 1986-1991, using official transition dates."""
    if not is_china_birthplace(birthplace):
        return False
    if local_dt.year == 1986:
        start = datetime(1986, 5, 4, 2)
        end = datetime(1986, 9, 14, 2)
    elif 1987 <= local_dt.year <= 1991:
        start = datetime(local_dt.year, 4, 1)
        while start.weekday() != 6:
            start += timedelta(days=1)
        if start.day < 11:
            start += timedelta(days=7)
        end = datetime(local_dt.year, 9, 1)
        while end.weekday() != 6:
            end += timedelta(days=1)
        if end.day < 11:
            end += timedelta(days=7)
        start = start.replace(hour=2)
        end = end.replace(hour=2)
    else:
        return False
    return start <= local_dt < end


def equation_of_time_minutes(dt):
    day_of_year = dt.timetuple().tm_yday
    angle = math.radians((360 / 365) * (day_of_year - 81))
    return 9.87 * math.sin(2 * angle) - 7.53 * math.cos(angle) - 1.5 * math.sin(angle)


def classify_zi_hour(true_solar_dt):
    if true_solar_dt.hour == 23:
        return '晚子时'
    if true_solar_dt.hour == 0:
        return '早子时'
    return None


def build_chart_context(year, month, day, time_text, birthplace, longitude,
                        summer_time_enabled=None):
    hour, minute, second, precision = parse_time_text(time_text)
    input_dt = datetime(year, month, day, hour, minute, second)
    if summer_time_enabled is None:
        summer_time_enabled = is_china_summer_time(input_dt, birthplace)
    standard_dt = input_dt - timedelta(hours=1) if summer_time_enabled else input_dt
    true_solar_offset = 4 * (float(longitude) - 120) + equation_of_time_minutes(standard_dt)
    true_solar_dt = standard_dt + timedelta(minutes=true_solar_offset)
    zi_hour_type = classify_zi_hour(true_solar_dt)
    return {
        'input_dt': input_dt,
        'standard_dt': standard_dt,
        'true_solar_dt': true_solar_dt,
        'true_solar_offset_minutes': true_solar_offset,
        'summer_time_enabled': bool(summer_time_enabled),
        'zi_hour_type': zi_hour_type,
        'final_day_date': true_solar_dt.date(),
        'final_hour_branch': '子' if zi_hour_type else _hour_branch(true_solar_dt.hour),
        'start_precision': precision,
        'qiyun_scheme': 3 if precision == 'second' else 2,
    }


def _hour_branch(hour):
    branches = ('子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥')
    return branches[((hour + 1) // 2) % 12]


def year_stem_is_yang(year_stem):
    return year_stem in ('甲', '丙', '戊', '庚', '壬')


def choose_qiyun_direction(year_stem, gender):
    """Return the internal direction used to select the adjacent jie."""
    if gender not in ('男', '女') or year_stem not in '甲乙丙丁戊己庚辛壬癸':
        raise ValueError('invalid year stem or gender')
    yang_year = year_stem_is_yang(year_stem)
    return 'forward' if (yang_year and gender == '男') or (not yang_year and gender == '女') else 'backward'


def calculate_qiyun(birth_dt, previous_jie, next_jie, year_stem, gender,
                    precision='hour'):
    """Calculate Luming start age from the selected adjacent jie.

    The caller supplies actual jie timestamps from the calendar base. Scheme 2
    uses hour precision; scheme 3 preserves minute/second precision.
    """
    direction = choose_qiyun_direction(year_stem, gender)
    target_jie = next_jie if direction == 'forward' else previous_jie
    if precision not in ('hour', 'minute', 'second'):
        raise ValueError('precision must be hour, minute, or second')
    delta = target_jie - birth_dt if direction == 'forward' else birth_dt - target_jie
    if delta.total_seconds() < 0:
        raise ValueError('target jie is on the wrong side of birth time')

    total_hours = delta.total_seconds() / 3600
    if precision == 'hour':
        total_hours = math.floor(total_hours)
    total_days = total_hours / 24
    years = int(total_days // 3)
    remainder_days = total_days - years * 3
    months = int(remainder_days * 4 // 1)
    remainder_days -= months / 4
    days = int(round(remainder_days * 30))
    start_dt = _add_calendar_age(birth_dt, years, months, days)
    return {
        'direction': direction,
        'target_jie': target_jie,
        'delta': delta,
        'precision': precision,
        'scheme': 2 if precision == 'hour' else 3,
        'years': years,
        'months': months,
        'days': days,
        'age_text': f'{years}岁{months}个月{days}天',
        'start_datetime': start_dt,
    }


def _add_calendar_age(dt, years, months, days):
    total_months = dt.year * 12 + (dt.month - 1) + years * 12 + months
    year, month_index = divmod(total_months, 12)
    month = month_index + 1
    if month == 2 and dt.day == 29:
        day = 28
    else:
        next_month = datetime(year + (month == 12), 1 if month == 12 else month + 1, 1)
        day = min(dt.day, (next_month - timedelta(days=1)).day)
    return dt.replace(year=year, month=month, day=day) + timedelta(days=days)


def build_luming_options(base_pillar, taiji_point, dayun_pillar, direction):
    allowed_pillars = {'年柱', '月柱', '日柱', '时柱'}
    if base_pillar not in allowed_pillars or dayun_pillar not in allowed_pillars:
        raise ValueError('invalid Luming pillar option')
    if direction not in ('顺排', '逆排'):
        raise ValueError('invalid Luming direction')
    if taiji_point not in '甲乙丙丁戊己庚辛壬癸':
        raise ValueError('invalid Taiji point')
    return {
        'base_pillar': base_pillar,
        'taiji_point': taiji_point,
        'dayun_pillar': dayun_pillar,
        'direction': direction,
    }


def build_snapshot(input_data, chart_context, result, *, rule_version='luming-draft.1', base_version='unfrozen'):
    return {
        'input': input_data,
        'context': chart_context,
        'result': result,
        'ruleVersion': rule_version,
        'baseVersion': base_version,
    }


def snapshot_json(snapshot):
    return json.dumps(snapshot, ensure_ascii=False, default=str, indent=2)


def generate_luming_dayun(pillars, options, qiyun, count=10):
    """Generate a selectable-pillar dayun sequence for the Luming draft path."""
    pillar_name = options['dayun_pillar']
    pillar = pillars.get(pillar_name)
    if not isinstance(pillar, str) or len(pillar) != 2:
        raise ValueError('selected dayun pillar is missing')
    stems = '甲乙丙丁戊己庚辛壬癸'
    branches = '寅卯辰巳午未申酉戌亥子丑'
    stem_index = stems.index(pillar[0])
    branch_index = branches.index(pillar[1])
    step = 1 if options['direction'] == '顺排' else -1
    rows = []
    for index in range(1, count + 1):
        rows.append({
            'index': index,
            'ganzhi': stems[(stem_index + step * index) % 10] + branches[(branch_index + step * index) % 12],
            'start_age': f'{qiyun["years"] + index - 1}岁',
            'source_pillar': pillar_name,
            'taiji_point': options['taiji_point'],
        })
    return rows


def save_snapshot(snapshot, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('w', encoding='utf-8') as stream:
        stream.write(snapshot_json(snapshot))
