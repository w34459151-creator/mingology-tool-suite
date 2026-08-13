import minggong_query_24jieqi as m

year = 1981
month = 12
day = 2
hour = 2

mdz, mn = m.get_month_dz(year, month, day)
print('month_dz', mdz, 'month_num', mn)
print('hour_dz', m.get_hour_dz(hour))
mg_dz = m.calc_minggong_dizhi(mn, m.get_hour_dz(hour))
print('minggong_dz', mg_dz)
print('birth_year_dz', m.get_year_dz(year))
print('start_branch', m.calc_yuexian_start_branch(m.get_year_dz(year), '巳', mg_dz))
yuexian = m.calc_yuexian('乙', '巳', m.get_year_dz(year), mg_dz)
print('yuexian:')
for month_name, tg, dz in yuexian:
    print(f'{month_name}: {tg}{dz}')
