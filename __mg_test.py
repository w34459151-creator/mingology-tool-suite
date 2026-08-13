import importlib.util
spec=importlib.util.spec_from_file_location('mg','c:/Users/Public/MyBookAnalysis/minggong_query_24jieqi.py')
mg=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mg)
# Test 1957-01-26 08:20
year,month,day,hour,minute=1957,1,26,8,20
month_dz,month_num=mg.get_month_dz(year,month,day,hour,minute)
hour_dz=mg.get_hour_dz(hour)
day_tg,day_dz=mg.calc_day_ganzhi(year,month,day)
print('1957 month_dz',month_dz,'month_num',month_num,'hour_dz',hour_dz)
print('day_pillar',day_tg+day_dz)
print('hour_pillar',mg.calc_hour_pillar(day_tg,hour))
print('minggong',mg.calc_minggong_dizhi(month_dz,hour_dz))
# Test 1981-12-02 02:00
year,month,day,hour,minute=1981,12,2,2,0
month_dz,month_num=mg.get_month_dz(year,month,day,hour,minute)
hour_dz=mg.get_hour_dz(hour)
print('1981 month_dz',month_dz,'month_num',month_num,'hour_dz',hour_dz)
print('minggong',mg.calc_minggong_dizhi(month_dz,hour_dz))
# check maqian/boshi existence
print('has maqian', hasattr(mg,'calc_maqian_12shen_for_year_branch'), 'has boshi', hasattr(mg,'calc_boshi_12shen'))
