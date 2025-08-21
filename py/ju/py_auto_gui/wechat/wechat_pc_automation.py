import time
import os
import random
import datetime
import schedule
import win32gui
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
import win32com.client
import pythoncom
import pygame

# 配置信息
WECHAT_TITLE = "微信"  # 微信窗口标题
MUSIC_FILE_PATH = r"D:\workspace\pycharm\PythonTest\py\ju\py_auto_gui\wechat\周杰伦 - 告白气球.mp3"  # 音乐文件路径


def connect_to_wechat():
    """连接到微信PC应用"""
    try:
        # 尝试连接到已运行的微信应用
        app = Application(backend="uia").connect(title_re=f"{WECHAT_TITLE}")
        main_window = app.window(title_re=f"{WECHAT_TITLE}")
        main_window.set_focus()
        print("成功连接到微信")
        return app, main_window
    except Exception as e:
        print(f"连接微信失败: {e}")
        print("尝试启动微信...")
        try:
            # 如果未运行，则启动微信
            app = Application(backend="uia").start("C:\\Program Files\\Tencent\\Weixin\\Weixin.exe")
            main_window = app.window(title_re=f"{WECHAT_TITLE}")
            # 等待微信启动
            main_window.wait("ready", timeout=5)
            main_window.set_focus()
            print("微信已启动")
            return app, main_window
        except Exception as e2:
            print(f"启动微信失败: {e2}")
            return None, None


def search_contact(main_window, contact_name):
    """搜索联系人"""
    try:
        # 点击搜索框
        search_box = main_window.child_window(title="搜索", control_type="Edit")
        search_box.wait("exists enabled visible", timeout=5)
        search_box.click_input()


        search_box.type_keys(contact_name)
        time.sleep(1)

        # 在搜索结果中选择联系人
        contact_item = main_window.child_window(title=contact_name, control_type="ListItem")
        if contact_item.exists():
            contact_item.click_input()
            print(f"已选择联系人: {contact_name}")
            return True
        else:
            print(f"未找到联系人: {contact_name}")
            return False
    except Exception as e:
        print(f"搜索联系人失败: {e}")
        return False


def initiate_voice_call(main_window):
    """发起语音通话"""
    try:
        # 点击聊天窗口中的"+"按钮
        # plus_button = main_window.child_window(title="更多功能按钮", control_type="Button")
        # plus_button.click_input()
        # time.sleep(1)

        # 点击语音通话按钮
        # 注意：按钮的名称可能因微信版本而异
        voice_call_button = main_window.child_window(title="语音聊天", control_type="Button")
        voice_call_button.click_input()
        print("已发起语音通话")
        return True
    except Exception as e:
        print(f"发起语音通话失败: {e}")
        return False


def wait_for_call_answer(main_window, timeout=600):
    """等待对方接听电话"""
    print(f"等待对方接听电话（超时时间: {timeout}秒）")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # 检查是否进入通话中状态
            # 通过查找通话中的挂断按钮判断
            hangup_button = main_window.child_window(title="挂断", control_type="Button")
            if hangup_button.exists():
                print("对方已接听电话")
                return True
            time.sleep(1)
        except:
            time.sleep(1)

    print("等待超时，对方未接听")
    return False


def play_music(music_path):
    """使用Windows Media Player播放音乐"""
    try:
        if not os.path.exists(music_path):
            print(f"音乐文件不存在: {music_path}")
            return False

        # 初始化COM库
        pythoncom.CoInitialize()

        # 创建Windows Media Player对象
        wmp = win32com.client.Dispatch("WMPlayer.OCX")
        player = wmp.newMedia(music_path)
        wmp.currentPlaylist.appendItem(player)
        wmp.controls.play()

        print(f"正在播放音乐: {os.path.basename(music_path)}")
        return True
    except Exception as e:
        print(f"播放音乐失败: {e}")
        return False
def play_media(music_path):
    pygame.mixer.init()

    # 加载音乐文件（替换为你的文件路径）
    music_path = music_path
    pygame.mixer.music.load(music_path)

    # 播放音乐
    # - loops: 循环次数（-1 表示无限循环）
    # - start: 从指定时间（秒）开始播放
    pygame.mixer.music.play(loops=0, start=0.0)

    # 保持程序运行，防止音乐中断
    try:
        while pygame.mixer.music.get_busy():  # 当音乐正在播放时
            pygame.time.Clock().tick(10)  # 每秒循环10次，降低CPU占用
    except KeyboardInterrupt:
        pygame.mixer.music.stop()  # 按 Ctrl+C 停止播放


def main():
    """主函数"""
    #contact_name = "王巨峰"  # 替换为实际联系人名称

    # 连接到微信
    app, main_window = connect_to_wechat()
    if not main_window:
        return

    # 搜索联系人
    # if not search_contact(main_window, contact_name):
    #     return

    # 发起语音通话
    if not initiate_voice_call(main_window):
        return

    # # 等待对方接听
    # if not wait_for_call_answer(main_window):
    #     # 超时未接听，尝试挂断
    #     try:
    #         cancel_button = main_window.child_window(title="取消", control_type="Button")
    #         cancel_button.click_input()
    #     except:
    #         pass
    #     return

    # 等待通话稳定
    time.sleep(5)

    # 播放音乐
    #play_music(MUSIC_FILE_PATH)

    # 保持程序运行，以便观察效果
    #input("按Enter键结束通话并退出程序...")
    time.sleep(3 * 60)
    # 结束通话
    try:
        hangup_button = main_window.child_window(title="挂断", control_type="Button")
        hangup_button.click_input()
        print("已结束通话")
    except Exception as e:
        print(f"结束通话失败: {e}")


def list_all_windows_with_pywinauto():
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):  # 只获取可见窗口
            print(win32gui.GetWindowText(hwnd))

    win32gui.EnumWindows(callback, None)
if __name__ == "__main__":
    #main()
    schedule.every().day.at("05:00").do(main)
    schedule.every().day.at("05:15").do(main)
    schedule.every().day.at("05:30").do(main)
    schedule.every().day.at("05:45").do(main)
    # schedule.every().day.at("06:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

