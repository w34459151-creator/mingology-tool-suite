import importlib.util
spec = importlib.util.spec_from_file_location('mg', r'c:\Users\Public\MyBookAnalysis\minggong_query_24jieqi.py')
mg = importlib.util.module_from_spec(spec)
# execute module safely (GUI guarded by __main__ now)
spec.loader.exec_module(mg)

year = 1981
month = 12
day = 2
hour = 2

print('Input: 1981-12-02 02:30 (using hour=2)')

year_tg = mg.get_year_tg(year)
year_dz = mg.get_year_dz(year)
month_dz, month_num = mg.get_month_dz(year, month, day)
month_tg = mg.get_month_tiangan(month_num, year_tg)
day_tg, day_dz = mg.calc_day_ganzhi(year, month, day)
hour_tg, hour_dz = mg.calc_hour_pillar(day_tg, hour)

print('Year pillar:', year_tg + year_dz)
print('Month pillar:', (month_tg or '?') + (month_dz or '?'))
print('Day pillar:', day_tg + day_dz)
print('Hour pillar:', hour_tg + hour_dz)

# Also check wuhu mapping for the computed month branch
wuhu = mg.get_wuhu_dun_month_tiangan(year_tg, month_dz)
print('Wuhu month stem mapping:', wuhu)
