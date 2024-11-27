import pyautogui
import pyperclip


# 将鼠标移动到屏幕中央
pyautogui.moveTo(pyautogui.size()[0]/2, pyautogui.size()[1]/2)

# 在屏幕中央单击鼠标左键
pyautogui.click()

# 将“Hello, world!”字符串键入计算机
pyautogui.typewrite('Hello, world!')
# 模拟按下键盘的A键
pyautogui.press('a')

# 模拟释放键盘的A键
pyautogui.release('a')

# 组合键
pyautogui.hotkey('ctrl', 'v')

# 截取整个屏幕
screenshot = pyautogui.screenshot()

# 显示截图
screenshot.show()