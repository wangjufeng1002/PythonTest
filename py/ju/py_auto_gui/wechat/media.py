import time

import pygame
import win32com.client
import pythoncom
import os


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




def play_music(music_path):
    """使用Windows Media Player播放音乐"""
    try:
        if not os.path.exists(music_path):
            print(f"音乐文件不存在: {music_path}")
            return False

        # 创建Windows Media Player对象
        wmp = win32com.client.Dispatch("WMPlayer.OCX")
        media = wmp.newMedia(music_path)

        wmp.currentMedia = media

        wmp.controls.play()  # 开始播放

        print(f"正在播放音乐: {os.path.basename(music_path)}")

        while True:

            time.sleep(5)
            print(wmp.status)  # 应输出 "Playing"
            print(wmp.controls.currentPosition)  # 应逐渐增大
        #input("按Enter键结束通话并退出程序...")
       # return True
    except Exception as e:
        print(f"播放音乐失败: {e}")
        return False




if __name__ == '__main__':
    #play_media("D:\workspace\pycharm\PythonTest\py\ju\py_auto_gui\wechat\周杰伦 - 告白气球.mp3")
    play_music("D:\\workspace\\pycharm\\PythonTest\\py\\ju\\py_auto_gui\\wechat\\周杰伦 - 告白气球.mp3")
