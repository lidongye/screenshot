#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye<dongye_bio@qq.com>
# 2019-08-01 14:29

import sys
import time
import win32gui, win32ui, win32con
from PIL import Image

args = sys.argv


def window_capture(window_name, filename):
    hwnd = win32gui.FindWindow("Notepad", window_name)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left + 1
    height = bottom - top + 1
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hwnd)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    # 保存图像到文件
    # saveBitMap.SaveBitmapFile(saveDC, filename)
    ###获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    im_PIL.show()  # 显示
    im_PIL.save(filename, "JPEG", quality=100)  # 保存
    im_PIL.show()  # 显示

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hWndDC)


def main(args):
    beg = time.time()
    window_capture(None, "./win32.jpg")
    end = time.time()
    print(end - beg)


if __name__ == '__main__':
    main(args)