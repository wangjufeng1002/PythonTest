from selenium import webdriver
import time
i = 0
while i<100:
    print(i)
    driver=webdriver.Chrome("C:\\Users\\JBS\Desktop\\test\\chromedriver_win32\\chromedriver.exe")
    driver.get('https://ding.fanqier.cn/f/xdmme3if')
    time.sleep(2)
    #王娇
    element = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/article/div/section/div[1]/div[2]/div/div[3]/ul/li[2]/div/div/label/span[1]')
    #
    element.click()
    # element = driver.find_element_by_xpath(
    #     '/html/body/div/div/div[3]/div/article/div/section/div[1]/div[2]/div/div[3]/ul/li[7]/div/div/label/span[1]')
    # element.click()
    time.sleep(1)
    sumbmit = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/article/div/section/div[2]/div/div/button')
    sumbmit.click()
    time.sleep(1)
    driver.close()
    i=i+1
# driver=webdriver.Chrome("C:\\Users\\JBS\Desktop\\test\\chromedriver_win32\\chromedriver.exe")
# driver.get('https://ding.fanqier.cn/f/xdmme3if')
# time.sleep(2)
# element = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/article/div/section/div[1]/div[2]/div/div[3]/ul/li[2]/div/div/label/span[1]')
# element.click()
# time.sleep(1)
# sumbmit = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/article/div/section/div[2]/div/div/button')
# sumbmit.click()
# time.sleep(2)
# driver.close()