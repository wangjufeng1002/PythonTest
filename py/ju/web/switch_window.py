import win32gui
import win32con


def switch_window(window_title):
    # 枚举窗口的回调函数
    def enum_windows_proc(hwnd, window_title):
        if win32gui.IsWindow(hwnd) and win32gui.GetWindowText(hwnd) == window_title:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 还原窗口
            win32gui.SetForegroundWindow(hwnd)  # 将窗口放到前台

    win32gui.EnumWindows(enum_windows_proc, window_title)

# switch_window("国家中小学智慧教育")
#
# text = win32gui.GetWindowText()
# print(text)



def get_all_windows(win_title):
    hwnd_title_map = {}

    def callback(hwnd, hwnd_title_map):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_title_map[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, hwnd_title_map)
    for hwnd, window_title in hwnd_title_map.items():
        if '国家中小学智慧教育平台' in window_title:
            win32gui.SetForegroundWindow(hwnd)  # 将窗口放到前台
    #         class_name = win32gui.GetClassName(hwnd)
    #         windows_list.append({'hwnd': hwnd, 'title': window_title, 'class': class_name})
    # return windows_list

#get_all_windows()






def get_all_windows_info():
    windows_list = []
    hwnd_title_map = {}

    def callback(hwnd, hwnd_title_map):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_title_map[hwnd] = win32gui.GetWindowText(hwnd)

    win32gui.EnumWindows(callback, hwnd_title_map)
    for hwnd, window_title in hwnd_title_map.items():
        if window_title:
            class_name = win32gui.GetClassName(hwnd)
            windows_list.append({'hwnd': hwnd, 'title': window_title, 'class': class_name})
    return windows_list


# 使用函数
all_windows = get_all_windows_info()
for window in all_windows:
    print(f"Handle: {window['hwnd']}, Title: {window['title']}, Class: {window['class']}")