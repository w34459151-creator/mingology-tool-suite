# -*- coding: utf-8 -*-
"""Final verification screenshots: capture each widget region (grid + flow-month strip).

IMPORTANT: On DPI-scaled displays, tkinter `winfo_*` logical coordinates can diverge
from physical screen pixels, so ImageGrab(bbox=widget coords) may capture a *different*
region than the widget (e.g. the grid instead of the strip). To verify widget content
reliably we capture each widget's OWN HWND via PrintWindow (WM_PRINT), which renders the
widget's content directly regardless of its on-screen position / DPI / occlusion.
"""
import os, sys, time, ctypes
import ctypes.wintypes
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
import tkinter as tk
from PIL import ImageGrab, Image

OUT = os.path.dirname(os.path.abspath(__file__))
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
PW_RENDERFULLCONTENT = 2


def _pw_bmp(hwnd, w, h):
    """PrintWindow a HWND into a PIL RGB image (physical render, DPI/position independent)."""
    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ('biSize', ctypes.wintypes.DWORD), ('biWidth', ctypes.c_long),
            ('biHeight', ctypes.c_long), ('biPlanes', ctypes.c_ushort),
            ('biBitCount', ctypes.c_ushort), ('biCompression', ctypes.wintypes.DWORD),
            ('biSizeImage', ctypes.wintypes.DWORD), ('biXPelsPerMeter', ctypes.c_long),
            ('biYPelsPerMeter', ctypes.c_long), ('biClrUsed', ctypes.wintypes.DWORD),
            ('biClrImportant', ctypes.wintypes.DWORD),
        ]
    class BITMAPINFO(ctypes.Structure):
        _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', ctypes.c_byte * 4)]
    hwnd_dc = user32.GetWindowDC(hwnd)
    mem_dc = gdi32.CreateCompatibleDC(hwnd_dc)
    bmp = gdi32.CreateCompatibleBitmap(hwnd_dc, w, h)
    gdi32.SelectObject(mem_dc, bmp)
    user32.PrintWindow(hwnd, mem_dc, PW_RENDERFULLCONTENT)
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem_dc, bmp, 0, h, buf, ctypes.byref(bmi), 0)
    img = Image.frombuffer('RGBA', (w, h), buf.raw, 'raw', 'BGRA', 0, 1).convert('RGB')
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mem_dc)
    user32.ReleaseDC(hwnd, hwnd_dc)
    return img


def grab_widget(widget, path):
    """Capture a widget's own rendered content via PrintWindow (DPI-safe)."""
    root = widget.winfo_toplevel()
    root.update_idletasks()
    root.update()
    time.sleep(0.15)
    img = _pw_bmp(widget.winfo_id(), widget.winfo_width(), widget.winfo_height())
    img.save(path)
    print('saved', path, img.size, '(PrintWindow of hwnd %d)' % widget.winfo_id())
    return img


def grab_window(root, path):
    """Whole-window screenshot via ImageGrab (context only, DPI-offset not critical)."""
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
    grab_widget(mod.ordinary_flow_grid, '_verify_ordinary_grid.png')
    grab_widget(mod.ordinary_flow_month_frame, '_verify_ordinary_strip.png')

    # 点击 2005 后的联动
    mod.ordinary_flow_grid._select_year(2005)
    root.update()
    grab_widget(mod.ordinary_flow_month_frame, '_verify_ordinary_strip_2005.png')

    # 禄命排盘：网格 + 流月条（太极点 癸）
    mod.query_luming()
    mod.result_notebook.select(mod.luming_result_frame)
    root.update()
    grab_window(root, '_verify_luming_window.png')
    grab_widget(mod.luming_flow_grid, '_verify_luming_grid.png')
    grab_widget(mod.luming_flow_month_frame, '_verify_luming_strip.png')
    mod.luming_flow_grid._select_year(2015)
    root.update()
    grab_widget(mod.luming_flow_month_frame, '_verify_luming_strip_2015.png')

    root.destroy()


if __name__ == '__main__':
    main()
