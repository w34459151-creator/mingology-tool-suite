import tkinter as tk
from tkinter import messagebox

# 支与干的度数表
dizhi_list = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
tiangan_list = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

def get_dizhi_num(dz):
    try:
        return dizhi_list.index(dz) + 1
    except ValueError:
        return None

def get_tiangan_num(tg):
    try:
        return tiangan_list.index(tg) + 1
    except ValueError:
        return None

def dizhi_by_num(num):
    return dizhi_list[(num - 1) % 12]

def tiangan_by_num(num):
    return tiangan_list[(num - 1) % 10]

# 计算命宫地支
# 太阳出卯算法：
# 以生月数（过了中气之后的那个月支的度数）与时支度数之和，
# 以 14 或 26 去减它们的和，结果调整到 1-12 之间。
def calc_minggong_dizhi(month_dz, hour_dz, base=26):
    m = get_dizhi_num(month_dz)
    h = get_dizhi_num(hour_dz)
    if m is None or h is None:
        return None
    s = base - (m + h)
    # 调整到 1..12
    while s <= 0:
        s += 12
    while s > 12:
        s -= 12
    return dizhi_by_num(s)

# 计算命宫天干（用五虎遁法，根据年干确定起月天干后按支位顺数）
def get_wuhu_start_tiangan(year_tg):
    y = get_tiangan_num(year_tg)
    if y is None:
        return None
    # 五虎遁：甲己丙，乙庚戊，丙辛庚，丁壬壬，戊癸甲
    mapping = {
        1: 3, 6: 3,  # 甲/己 -> 丙
        2: 5, 7: 5,  # 乙/庚 -> 戊
        3: 7, 8: 7,  # 丙/辛 -> 庚
        4: 9, 9: 9,  # 丁/壬 -> 壬
        5: 1, 10: 1, # 戊/癸 -> 甲
    }
    return mapping.get(y)

def calc_minggong_tiangan(year_tg, minggong_dz):
    start = get_wuhu_start_tiangan(year_tg)
    d = get_dizhi_num(minggong_dz)
    if start is None or d is None:
        return None
    # 支位从寅开始算起（寅=1）
    offset = d - 1
    s = start + offset
    while s > 10:
        s -= 10
    return tiangan_by_num(s)

# 这些变量将在程序启动时赋值（避免 import 时创建 tk 变量）
after_zhongqi_var = None
base_var = None


def query_minggong():
    year_tg = entry_year_tg.get().strip()
    month_dz = entry_month_dz.get().strip()
    hour_dz = entry_hour_dz.get().strip()
    birthplace = entry_birthplace.get().strip()
    base = int(base_var.get())
    after_zhongqi = after_zhongqi_var.get()
    if not (year_tg and month_dz and hour_dz):
        messagebox.showerror('错误', '请填写完整的年干、月支、时支')
        return
    if after_zhongqi:
        # 24节气中，第二个节气为中气；若命主出生在中气后，则视为下一个月支
        mnum = get_dizhi_num(month_dz)
        if mnum is None:
            messagebox.showerror('错误', '月支输入有误')
            return
        month_dz = dizhi_by_num(mnum + 1)
    mg_dz = calc_minggong_dizhi(month_dz, hour_dz, base=base)
    if mg_dz is None:
        messagebox.showerror('错误', '月支或时支输入有误')
        return
    mg_tg = calc_minggong_tiangan(year_tg, mg_dz)
    if mg_tg is None:
        messagebox.showerror('错误', '年干输入有误')
        return
    if birthplace:
        result = f'命宫：{mg_tg}{mg_dz}  (基数={base})\n出生地：{birthplace}'
    else:
        result = f'命宫：{mg_tg}{mg_dz}  (基数={base})'
    messagebox.showinfo('查询结果', result)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('命宫查询')

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    label_year_tg = tk.Label(frame, text='年干（如甲、乙...）:')
    label_year_tg.grid(row=0, column=0, sticky='e')
    entry_year_tg = tk.Entry(frame)
    entry_year_tg.grid(row=0, column=1)

    label_month_dz = tk.Label(frame, text='月支（如寅、卯...）:')
    label_month_dz.grid(row=1, column=0, sticky='e')
    entry_month_dz = tk.Entry(frame)
    entry_month_dz.grid(row=1, column=1)

    label_hour_dz = tk.Label(frame, text='时支（如寅、卯...）:')
    label_hour_dz.grid(row=2, column=0, sticky='e')
    entry_hour_dz = tk.Entry(frame)
    entry_hour_dz.grid(row=2, column=1)

    label_birthplace = tk.Label(frame, text='出生地:')
    label_birthplace.grid(row=3, column=0, sticky='e')
    entry_birthplace = tk.Entry(frame)
    entry_birthplace.grid(row=3, column=1)

    # 24节气的第二个节气是中气
    after_zhongqi_var = tk.BooleanVar(value=False)
    chk_zhongqi = tk.Checkbutton(frame, text='出生在中气后（视为下一个月支）', variable=after_zhongqi_var)
    chk_zhongqi.grid(row=4, column=0, columnspan=2, sticky='w', pady=(4, 4))

    label_base = tk.Label(frame, text='基数 (14/26):')
    label_base.grid(row=5, column=0, sticky='e')
    base_var = tk.StringVar(value='26')
    option_base = tk.OptionMenu(frame, base_var, '14', '26')
    option_base.grid(row=5, column=1, sticky='w')

    btn_query = tk.Button(frame, text='查询命宫', command=query_minggong)
    btn_query.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()
