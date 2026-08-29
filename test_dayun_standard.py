"""
自测：普通排盘·大运（calc_dayun_standard），验证 lunar_python 官方大运序列输出。
测试数据：1981年12月2日2时，男，出生地：湖北省十堰市房县。
仅验证新增函数，不涉及界面，未接入任何现有查询流程。
"""
import importlib
import sys
import tkinter as tk

tk.Tk.mainloop = lambda self, *a, **kw: None


def main():
    mod = importlib.import_module('minggong_query_24jieqi')

    mod.entry_year.delete(0, tk.END); mod.entry_year.insert(0, '1981')
    mod.entry_month.delete(0, tk.END); mod.entry_month.insert(0, '12')
    mod.entry_day.delete(0, tk.END); mod.entry_day.insert(0, '2')
    mod.entry_hour.delete(0, tk.END); mod.entry_hour.insert(0, '2')
    mod.gender_var.set('男')
    mod.var.set('阳历')
    mod._set_birthplace_text('湖北省十堰市房县')

    solar_ctx = mod.build_true_solar_context(1981, 12, 2, 2, 0, '湖北省十堰市房县')
    true_dt = solar_ctx['true_dt']
    print(f'真太阳时: {true_dt}')

    result = mod.calc_dayun_standard(true_dt, '男', sect=2, count=10)
    assert result is not None, 'lunar_python 不可用，calc_dayun_standard 返回 None'

    print(f"顺逆: {'顺排' if result['forward'] else '逆排'}")
    print(f"起运: 出生后{result['start_year']}年{result['start_month']}月{result['start_day']}天{result['start_hour']}小时")
    print(f"起运日期: {result['start_date']}")
    print('\n大运序列:')
    print(f"{'序号':<4}{'干支':<6}{'起始年龄':<8}{'结束年龄':<8}{'起始年份':<8}{'结束年份':<8}")
    for row in result['dayun']:
        print(f"{row['index']:<4}{row['ganzhi']:<6}{row['start_age']:<8}{row['end_age']:<8}{row['start_year']:<8}{row['end_year']:<8}")

    # 与已知参照（现有 build_zhiyi_extra_info 输出的"交运"信息）核对第一步大运
    assert result['dayun'][0]['ganzhi'] == '戊戌', f"第一步大运应为戊戌（与现有交运提示一致），实际 {result['dayun'][0]['ganzhi']}"
    assert result['dayun'][0]['start_age'] == 9, f"第一步大运起始年龄应为9岁（与现有交运提示一致），实际 {result['dayun'][0]['start_age']}"
    assert len(result['dayun']) == 10, f"应返回10步大运，实际 {len(result['dayun'])}"

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
