import minggong_query_24jieqi as m

print('start for 乙:', m.get_wuhu_dun_start_tiangan('乙'))
for i in range(1, 13):
    print(i, m.get_wuhu_dun_month_tiangan('乙', i))
