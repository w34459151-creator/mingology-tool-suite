# -*- coding: utf-8 -*-
"""Final verification screenshots: capture each widget region (grid + flow-month strip)."""
import os, sys, time
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
import tkinter as tk
from PIL import ImageGrab

OUT = os.path.dirname(os.path.abspath(__file__))


def grab_bbox(widget, path, pad=6):
    root = widget.winfo_toplevel()
    root.update_idletasks()
    root.update()
    time.sleep(0.15)
    x0 = widget.winfo_rootx() - pad
    y0 = widget.winfo_rooty() - pad
    x1 = x0 + widget.winfo_width() + pad * 2
    y1 = y0 + widget.winfo_height() + pad * 2
    img = ImageGrab.grab(bbox=(x0, y0, x1, y1))
    img.save(path)
    print('saved', path, img.size, 'bbox', (x0, y0, x1, y1))


def grab_window(root, path):
    root.attributes('-topmost', True)
    for _ in range(2):
        root.update()
        time.sleep(0.12)
    img = ImageGrab.grab(bbox=(root.winfo_rootx(), root.winfo_rooty(),
                               root.winfo_rootx() + root.winfo_width(),
                               root.winfo_rooty() + root.winfo_height()))
    root.attributes('-topmost', False)
    img.save(path)
    print('saved', path, img.size)


def main():
    mod = __import__('minggong_query_24jieqi')
    root = mod.root
    try:
        root.state('normal')
    except tk.TclError:
        pass
    root.geometry('1500x960+20+20')

    def set_birthplace(text):
        mod.entry_birthplace.config(state='normal')
        mod.entry_birthplace.delete(0, tk.END)
        mod.entry_birthplace.insert(0, text)
        mod.entry_birthplace.config(state='readonly')
        mod.refresh_summer_time_suggestion()

    mod.entry_year.delete(0, tk.END); mod.entry_year.insert(0, '1981')
    mod.entry_month.delete(0, tk.END); mod.entry_month.insert(0, '12')
    mod.entry_day.delete(0, tk.END); mod.entry_day.insert(0, '2')
    mod.entry_hour.delete(0, tk.END); mod.entry_hour.insert(0, '02:00')
    mod.gender_var.set('男')
    mod.var.set('阳历')
    set_birthplace('湖北省十堰市房县')
    root.update()

    # 先进入结果页（自动跳转），再切到普通排盘页签
    mod.start_chart_query()
    root.update()

    # 普通排盘：网格 + 流月条（默认 2026）
    mod.query_ordinary()
    mod.result_notebook.select(mod.ordinary_result_frame)
    root.update()
    grab_window(root, '_verify_ordinary_window.png')
    grab_bbox(mod.ordinary_flow_grid, '_verify_ordinary_grid.png')
    grab_bbox(mod.ordinary_flow_month_frame, '_verify_ordinary_strip.png')

    # 点击 2005 后的联动
    mod.ordinary_flow_grid._select_year(2005)
    root.update()
    grab_bbox(mod.ordinary_flow_month_frame, '_verify_ordinary_strip_2005.png')

    # 禄命排盘：网格 + 流月条（太极点 癸）
    mod.query_luming()
    mod.result_notebook.select(mod.luming_result_frame)
    root.update()
    grab_window(root, '_verify_luming_window.png')
    grab_bbox(mod.luming_flow_grid, '_verify_luming_grid.png')
    grab_bbox(mod.luming_flow_month_frame, '_verify_luming_strip.png')
    mod.luming_flow_grid._select_year(2015)
    root.update()
    grab_bbox(mod.luming_flow_month_frame, '_verify_luming_strip_2015.png')

    root.destroy()


if __name__ == '__main__':
    main()