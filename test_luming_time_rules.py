from datetime import datetime
import traceback
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import tempfile

import luming_time_rules as rules


def test_time_precision_selects_qiyun_scheme():
    assert rules.parse_time_text('2')[3] == 'hour'
    assert rules.parse_time_text('2:30')[3] == 'minute'
    assert rules.parse_time_text('2:30:15')[3] == 'second'

    hour_context = rules.build_chart_context(1981, 12, 2, '2', '湖北省十堰市房县', 110.7358)
    second_context = rules.build_chart_context(1981, 12, 2, '2:30:15', '湖北省十堰市房县', 110.7358)
    assert hour_context['qiyun_scheme'] == 2
    assert second_context['qiyun_scheme'] == 3


def test_china_only_historical_summer_time():
    assert rules.is_china_summer_time(datetime(1986, 5, 4, 1, 59), '贵州省黔东南州') is False
    assert rules.is_china_summer_time(datetime(1986, 5, 4, 2, 0), '贵州省黔东南州') is True
    assert rules.is_china_summer_time(datetime(1992, 5, 4, 12), '贵州省黔东南州') is False
    assert rules.is_china_summer_time(datetime(1986, 5, 4, 12), '日本东京') is False


def test_zi_hour_classification_uses_true_solar_time():
    assert rules.classify_zi_hour(datetime(1981, 12, 2, 23, 0)) == '晚子时'
    assert rules.classify_zi_hour(datetime(1981, 12, 3, 0, 0)) == '早子时'
    assert rules.classify_zi_hour(datetime(1981, 12, 3, 1, 0)) is None


def test_summer_time_is_removed_before_true_solar_calculation():
    context = rules.build_chart_context(
        1986, 5, 4, '2:00:00', '贵州省黔东南州', 107.9775
    )
    assert context['summer_time_enabled'] is True
    assert context['standard_dt'] == datetime(1986, 5, 4, 1, 0)
    assert context['true_solar_dt'].hour == 0
    assert context['final_hour_branch'] == '子'


def test_qiyun_direction_and_precision_are_gender_aware():
    birth = datetime(1981, 12, 2, 2, 30, 15)
    previous_jie = datetime(1981, 11, 8, 1, 0, 0)
    next_jie = datetime(1981, 12, 7, 12, 0, 0)

    male = rules.calculate_qiyun(birth, previous_jie, next_jie, '辛', '男', 'hour')
    female = rules.calculate_qiyun(birth, previous_jie, next_jie, '辛', '女', 'second')
    assert male['direction'] == 'backward'
    assert male['target_jie'] == previous_jie
    assert female['direction'] == 'forward'
    assert female['target_jie'] == next_jie
    assert male['scheme'] == 2
    assert female['scheme'] == 3


def test_luming_options_and_snapshot_are_structured():
    options = rules.build_luming_options('日柱', '癸', '月柱', '顺排')
    snapshot = rules.build_snapshot(
        {'gender': '女'}, {'zi_hour_type': '早子时'},
        {'qiyun': {'age_text': '3岁2个月'}},
        rule_version='luming-test.1', base_version='lunar-test',
    )
    assert options == {
        'base_pillar': '日柱', 'taiji_point': '癸',
        'dayun_pillar': '月柱', 'direction': '顺排',
    }
    assert rules.snapshot_json(snapshot).find('luming-test.1') >= 0


def test_luming_dayun_uses_selected_pillar_and_direction(tmp_path):
    options = rules.build_luming_options('日柱', '癸', '月柱', '逆排')
    rows = rules.generate_luming_dayun(
        {'年柱': '辛酉', '月柱': '庚子', '日柱': '甲寅', '时柱': '乙丑'},
        options, {'years': 3}, count=2,
    )
    assert [row['ganzhi'] for row in rows] == ['己亥', '戊戌']
    assert rows[0]['source_pillar'] == '月柱'
    path = tmp_path / 'snapshot.json'
    rules.save_snapshot({'result': rows}, path)
    assert '己亥' in path.read_text(encoding='utf-8')

    def test_snapshot_save_creates_json_file(tmp_path):
        path = tmp_path / 'nested' / 'snapshot.json'
        rules.save_snapshot({'zi_hour_type': '晚子时'}, path)
        assert path.exists()
        assert '晚子时' in path.read_text(encoding='utf-8')
    lambda: test_snapshot_save_creates_json_file(Path(tempfile.mkdtemp())),


def main():
    tests = [
        test_time_precision_selects_qiyun_scheme,
        test_china_only_historical_summer_time,
        test_zi_hour_classification_uses_true_solar_time,
        test_summer_time_is_removed_before_true_solar_calculation,
        test_qiyun_direction_and_precision_are_gender_aware,
        test_luming_options_and_snapshot_are_structured,
        lambda: test_luming_dayun_uses_selected_pillar_and_direction(Path(tempfile.mkdtemp())),
    ]
    print('禄命时间规则测试开始')
    passed = 0
    for test in tests:
        try:
            test()
        except Exception:
            print(f'[失败] {test.__name__}')
            traceback.print_exc()
            continue
        passed += 1
        print(f'[通过] {test.__name__}')
    print(f'测试结果：{passed}/{len(tests)} 通过')
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo('禄命时间规则测试', f'测试结果：{passed}/{len(tests)} 通过')
        root.destroy()
    except tk.TclError:
        pass
    return passed == len(tests)


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
