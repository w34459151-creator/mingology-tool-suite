"""
无界面回归测试：验证摘要分组换行(format_summary_lines)调整后，
月限12神表格取数逻辑与展示内容未发生变化。
测试数据：1981年12月2日2时，男，出生地：湖北省十堰市房县。

注意：双击本文件会用系统关联的 python.exe 打开，运行结束后窗口会立刻关闭（一闪而过）。
请双击同目录下的 run_test_summary_layout.bat 来运行，它会在结束后暂停窗口。
"""
import importlib
import sys
import tkinter as tk

# 阻止 mainloop 阻塞，让模块顶层代码执行完毕后立即返回
tk.Tk.mainloop = lambda self, *a, **kw: None

def main():
    mod = importlib.import_module('minggong_query_24jieqi')

    # 填入测试数据
    mod.entry_year.delete(0, tk.END); mod.entry_year.insert(0, '1981')
    mod.entry_month.delete(0, tk.END); mod.entry_month.insert(0, '12')
    mod.entry_day.delete(0, tk.END); mod.entry_day.insert(0, '2')
    mod.entry_hour.delete(0, tk.END); mod.entry_hour.insert(0, '2')
    mod.gender_var.set('女')
    mod.var.set('阳历')
    mod._set_birthplace_text('湖北省十堰市房县')

    def print_block(title, text):
        print(f'\n=== {title} ===')
        for line in text.split('\n'):
            print(f'  | {line}')

    def print_table(table):
        cols = table['columns']
        rows = [table.item(i)['values'] for i in table.get_children()]
        widths = [max(len(str(c)), *(len(str(r[i])) for r in rows)) for i, c in enumerate(cols)]
        def fmt_row(vals):
            return ' | '.join(str(v).ljust(w) for v, w in zip(vals, widths))
        print(fmt_row(cols))
        print('-+-'.join('-' * w for w in widths))
        for r in rows:
            print(fmt_row(r))

    # 1) 命宫查询
    mod.query_minggong()
    minggong_text = mod.result_info_label['text']
    print_block('命宫查询结果（result_info_label）', minggong_text)
    assert '标准时' in minggong_text and '真太阳时修正量' in minggong_text
    summary_part = minggong_text.split('\n\n', 1)[0]
    print(f'\n摘要部分行数: {summary_part.count(chr(10)) + 1}')
    assert summary_part.count('\n') < 12, f"摘要行数未减少，仍有 {summary_part.count(chr(10)) + 1} 行"

    # 2) 月限神煞查询
    mod.query_yuexian()
    summary_text = mod.result_info_label['text']
    print_block('月限神煞摘要（result_info_label）', summary_text)
    assert '本命年柱' in summary_text
    assert summary_text.count('\n') < 8, f"行数未减少，仍有 {summary_text.count(chr(10))} 行"

    rows = mod.result_table.get_children()
    print(f'\n表格行数: {len(rows)}')
    assert len(rows) == 10, f"期望10行，实际 {len(rows)}"
    first_row_values = mod.result_table.item(rows[0])['values']
    assert len(first_row_values) == 13, f"期望13列(项目+12月)，实际 {len(first_row_values)}"
    print('\n=== 月限12神完整表格 ===')
    print_table(mod.result_table)

    # 3) 五虎遁（日柱/时柱周围的遁干/遁支）
    year_pillar_str = mod.entry_year_pillar.get()
    day_pillar_str = mod.entry_day_pillar.get()
    hour_pillar_str = mod.entry_hour_pillar.get()
    print(f'\n年柱: {year_pillar_str}  日柱: {day_pillar_str}  时柱: {hour_pillar_str}')
    print(f"日柱遁干: {mod.entry_day_pillar.dun_gan_label['text']}  日柱遁支: {mod.entry_day_pillar.dun_zhi_label['text']}")
    print(f"时柱遁干: {mod.entry_hour_pillar.dun_gan_label['text']}  时柱遁支: {mod.entry_hour_pillar.dun_zhi_label['text']}")
    assert year_pillar_str == '辛酉' and day_pillar_str == '甲寅' and hour_pillar_str == '乙丑'
    assert mod.entry_day_pillar.dun_gan_label['text'] == '甲午', mod.entry_day_pillar.dun_gan_label['text']
    assert mod.entry_day_pillar.dun_zhi_label['text'] == '庚寅', mod.entry_day_pillar.dun_zhi_label['text']
    assert mod.entry_hour_pillar.dun_gan_label['text'] == '乙未', mod.entry_hour_pillar.dun_gan_label['text']
    assert mod.entry_hour_pillar.dun_zhi_label['text'] == '辛丑', mod.entry_hour_pillar.dun_zhi_label['text']

    print('\n全部测试通过')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        input('\n测试结束，按回车键关闭窗口...')
