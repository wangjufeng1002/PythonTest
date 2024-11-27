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



# 将鼠标移动到屏幕中央
pyautogui.moveTo(pyautogui.size()[0]/2, pyautogui.size()[1]/2)

# 在屏幕中央单击鼠标左键
pyautogui.click()