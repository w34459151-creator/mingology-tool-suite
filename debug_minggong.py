import importlib.util
spec = importlib.util.spec_from_file_location('mg', 'C:/Users/Public/MyBookAnalysis/minggong_query_24jieqi.py')
mg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)

lunar_year, lunar_month, lunar_day, hour = 1981, 11, 7, 1
solar = mg.lunar_to_solar(lunar_year, lunar_month, lunar_day, False)
print('solar', solar)
month_dz, month_num = mg.get_month_dz(*solar)
print('month_dz', month_dz, 'month_num', month_num)
print('hour_dz', mg.get_hour_dz(hour))
year_tg = mg.get_year_tg(solar[0])
print('year_tg', year_tg)
mg_dz = mg.calc_minggong_dizhi(month_num, mg.get_hour_dz(hour))
mg_tg = mg.calc_minggong_tiangan(year_tg, mg_dz)
print('minggong', mg_tg + mg_dz)
