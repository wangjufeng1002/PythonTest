from selenium import  webdriver

import  time

edge = webdriver.Edge()

url = "https://topik.neea.edu.cn/"

edge.get(url)


while (True):
    time.sleep(10)
    edge.refresh()

