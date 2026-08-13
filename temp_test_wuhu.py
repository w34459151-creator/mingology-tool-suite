from minggong_query_24jieqi import calc_yuexian

seq = calc_yuexian('丙', '午', '午', '卯')
for m, tg, dz in seq:
    print(f'{m} {tg}{dz}')
