# coding=utf-8
import time

import uvicorn
import win32con
import win32gui
from fastapi import FastAPI

app = FastAPI()


@app.get("/switch")
async def switch():
    hwnd_title_map = {}
    target_hwnd = None
    back_hwnd = None

    def callback(hwnd, hwnd_title_map):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_title_map[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, hwnd_title_map)

    top_page_hwnd = win32gui.GetForegroundWindow()
    if '国家中小学智慧教育平台' in hwnd_title_map[top_page_hwnd]:
        return "success"

    for hwnd, window_title in hwnd_title_map.items():
        if '国家中小学智慧教育平台' in window_title:
            target_hwnd = hwnd

        if 'jbs' in window_title:
            back_hwnd = hwnd
    win32gui.ShowWindow(target_hwnd, win32con.SW_MAXIMIZE)


    return "success"


@app.get("/down")
async def down():
    hwnd_title_map = {}
    target_hwnd = None
    back_hwnd = None

    def callback(hwnd, hwnd_title_map):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_title_map[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, hwnd_title_map)

    top_page_hwnd = win32gui.GetForegroundWindow()
    if '国家中小学智慧教育平台' in hwnd_title_map[top_page_hwnd]:
        return "success"

    for hwnd, window_title in hwnd_title_map.items():
        if '国家中小学智慧教育平台' in window_title:
            target_hwnd = hwnd

        if 'jbs' in window_title:
            back_hwnd = hwnd
    win32gui.ShowWindow(target_hwnd, win32con.SW_MINIMIZE)

    return "success"


if __name__ == '__main__':
    # server = pywsgi.WSGIServer(('0.0.0.0', 29082), app, handler_class=WebSocketHandler)
    # server.serve_forever()
    # print("aaa")

    uvicorn.run(app='auto_look_fast:app', host="0.0.0.0", port=29081, workers=1)

    # win32gui.ShowWindow(15276314, win32con.SW_MAXIMIZE)
    # time.sleep(3)
    # win32gui.ShowWindow(15276314, win32con.SW_MINIMIZE)
