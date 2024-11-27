import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def login(web_driver):
    web_driver.get("https://basic.smartedu.cn/training/5d7cf98c-3a42-4b13-8e5f-56f40ce08b1d")
    while True:
        login_button = web_driver.find_element(By.XPATH,
                                               '//*[@id="header"]/div/div[2]/div[2]/div[2]/div[3]/div/a[1]/div')
        if login_button is not None:
            login_button.click()
            break

    while True:
        user_name = web_driver.find_element(By.ID, 'username')
        if user_name is not None:
            user_name.send_keys("18291532887")
            # liujuan123
            break
    while True:
        pass_word = web_driver.find_element(By.ID, 'tmpPassword')
        if pass_word is not None:
            pass_word.send_keys("liujuan123")
            break
    checkBox = web_driver.find_element(By.ID, "agreementCheckbox")
    if checkBox.is_selected() is False:
        checkBox.click()

    while True:
        login_btn = web_driver.find_element(By.ID, "loginBtn")
        print(login_btn is None)
        if login_btn is not None:
            login_btn.click()
            break


if __name__ == '__main__':
    options = Options()
    # 开启无界面模式
    options.add_argument("--headless")
    # 可选项：禁用GPU，可以解决一些莫名的问题
    options.add_argument("--disable-gpu")
    # 保持浏览器不关闭
    options.add_experimental_option('detach', True)
    service = Service(executable_path=r'D:\software-install-pk\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    login(web_driver=driver)

    time.sleep(10)
    driver.quit()
