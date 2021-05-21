from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver import ActionChains

#初始
def main():
    bro = webdriver.Chrome("D:\安装包\chromedriver_win32\chromedriver.exe")
    #bro = webdriver.Chrome()
    bro.maximize_window()

    bro.get("https://login.taobao.com/member/login.jhtml")
    time.sleep(1)

    bro.find_element_by_name("fm-login-id").send_keys("15091751738")
    time.sleep(1)
    bro.find_element_by_name("fm-login-password").send_keys("wf0328ju-+")
    time.sleep(1)

    GetImage(bro)

#===================================================================================

#获取
def GetImage(bro):
    # save_screenshot 就是将当前页面进行截图且保存
    #bro.save_screenshot('taobao.png')

    #code_img_ele = bro.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
    code_img_ele = bro.find_element_by_class_name("nc_iconfont btn_slide")
    Action(bro,code_img_ele)

#===================================================================================

#执行
def Action(bro,code_img_ele):
    # 动作链
    action = ActionChains(bro)
    # 长按且点击
    action.click_and_hold(code_img_ele)

    # move_by_offset(x,y) x水平方向,y竖直方向
    # perform()让动作链立即执行
    action.move_by_offset(300, 0).perform()
    time.sleep(0.5)

    # 释放动作链
    action.release()
    # 登录
    bro.find_element_by_xpath("//*[@id='login-form']/div[4]/button").click()
    time.sleep(10)
    bro.quit() #关闭浏览器

if __name__ == "__main__":
    main()
