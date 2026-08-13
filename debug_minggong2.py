import importlib.util
spec = importlib.util.spec_from_file_location('mg', 'C:/Users/Public/MyBookAnalysis/minggong_query_24jieqi.py')
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

# Test case: 1981-12-2 01:00 (公历)
year, month, day, hour = 1981, 12, 2, 1

solar = (year, month, day)
month_dz, month_num = mg.get_month_dz(year, month, day)
print('solar:', solar)
print('computed month_num:', month_num, 'month_dz:', month_dz)
print('hour_dz:', mg.get_hour_dz(hour), 'hour_idx:', mg.get_dizhi_num(mg.get_hour_dz(hour)))

year_tg = mg.get_year_tg(year)
print('year_tg:', year_tg)

mg_dz = mg.calc_minggong_dizhi(month_num, mg.get_hour_dz(hour))
mg_tg = mg.calc_minggong_tiangan(year_tg, mg_dz)
print('命宫:', mg_tg + mg_dz)
