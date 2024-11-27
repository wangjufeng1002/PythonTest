import time
import random
import traceback
import clipboard
import pyautogui
import pyautogui as pag
import requests
import tween
import numpy as np
import logging
import time

import pandas
import xlrd
import xlwt
import xlsxwriter


def get_screenshot():
    pyautogui.moveTo(1421, 64, duration=1)
    pyautogui.click()
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    clipboard.copy(
        "https://detail.tmall.com/item.htm?abbucket=2&ft=t,t&id=669225369630&ns=1&skuId=5028961721857&spm=a21n57.1.0.0.7742523cwMpeC3")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    time.sleep(3)
    search_box = pyautogui.locateOnScreen('gou.png', confidence=0.7, grayscale=True)
    search_box_center = pyautogui.center(search_box)
    pyautogui.moveTo(search_box_center.x + 50, search_box_center.y, duration=1)  # 移动鼠标
    time.sleep(1)
    screenshot = pyautogui.screenshot(region=(356, 367, 1300, 500), imageFilename="669225369630-5028961721857.png")
    screenshot.save("E:\\taobao-price\\669225369630-5028961721857.png")


if __name__ == '__main__':
    # pyautogui.press('win')
    # pyautogui.write('chrome')
    # time.sleep(1)
    # pyautogui.press('enter')

    # # 等待浏览器打开
    # time.sleep(5)
    # search_box = pyautogui.locateOnScreen('chrome-user.png', confidence=0.7, grayscale=True)
    # search_box_center = pyautogui.center(search_box)
    # pyautogui.moveTo(search_box_center, duration=1)  # 移动鼠标
    # pyautogui.click()  # 点击传回的坐标
    #
    # time.sleep(1)

    get_screenshot()

    time.sleep(100)

def getSkuId():
    # 读取excel
    workbook = xlrd.open_workbook("D:\\项目相关\\fms\\4.3.2\\8.31代发仓库存及单价处理后.xlsx")
    sheets_ = workbook.sheets()[0]
    rows = sheets_.nrows
    count_1 = 0


