"""真太阳时与四柱的回归测试。"""
import importlib
import json
import tkinter as tk
from datetime import datetime


tk.Tk.mainloop = lambda self, *args, **kwargs: None


def test_kaili_case():
    mod = importlib.import_module('minggong_query_24jieqi')
    place = '贵州省黔东南苗族侗族自治州凯里市'
    context = mod.build_true_solar_context(2000, 6, 9, 9, 20, place)

    assert context['used_true_solar'] is True
    assert context['longitude'] == 107.9775
    assert context['true_dt'].strftime('%Y-%m-%d %H:%M') == '2000-06-09 08:32'

    pillars = mod.calc_bazi_pillars_with_true_solar(2000, 6, 9, 9, 20, place)
    assert [pillars[key] for key in ('year_pillar', 'month_pillar', 'day_pillar', 'hour_pillar')] == [
        '庚辰', '壬午', '戊戌', '丙辰'
    ]


def test_location_record_has_coordinates():
    with open('address_library.json', encoding='utf-8') as stream:
        payload = json.load(stream)

    entry = next(
        row for row in payload['entries']
        if row.get('name') == '贵州省黔东南苗族侗族自治州凯里市'
    )
    assert isinstance(entry['latitude'], (int, float))
    assert isinstance(entry['longitude'], (int, float))


def test_true_solar_datetime_can_cross_day_boundary():
    mod = importlib.import_module('minggong_query_24jieqi')
    context = mod.build_true_solar_context(2000, 6, 9, 0, 20, '新疆乌鲁木齐市沙依巴克区')

    assert context['used_true_solar'] is True
    assert context['true_dt'].date().isoformat() == '2000-06-08'


def test_china_historical_daylight_time_is_detected_and_removed():
    mod = importlib.import_module('minggong_query_24jieqi')

    assert mod.is_china_summer_time(datetime(1986, 5, 4, 1, 59), '贵州省黔东南州') is False
    assert mod.is_china_summer_time(datetime(1986, 5, 4, 2, 0), '贵州省黔东南州') is True

    context = mod.build_true_solar_context(1986, 5, 4, 2, 0, '贵州省黔东南州')
    assert context['summer_time_enabled'] is True
    assert context['standard_dt'].strftime('%Y-%m-%d %H:%M') == '1986-05-04 01:00'


def test_explicit_standard_time_overrides_automatic_daylight_time():
    mod = importlib.import_module('minggong_query_24jieqi')
    context = mod.build_true_solar_context(1986, 5, 4, 2, 0, '贵州省黔东南州', False)

    assert context['summer_time_enabled'] is False
    assert context['standard_dt'] == context['input_dt']
