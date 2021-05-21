from tkinter import Image
from selenium import webdriver
from time import sleep, time
import requests
from selenium.webdriver import ActionChains

chrome = webdriver.Chrome("D:\安装包\chromedriver_win32\chromedriver.exe")
chrome.get("https://www.taobao.com/")
loginButton= chrome.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]')
loginButton.click()
while 1:
    username = chrome.find_element_by_xpath('//*[@id="fm-login-id"]')
    if username is not None:
        break
chrome.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys('15091751738')
chrome.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys('WF0328ju-+')
sleep(1)
if chrome.find_element_by_xpath('//*[@id="nc_2__scale_text"]/span') is not None:
    click = chrome.find_element_by_xpath('//*[@id="nc_2_n1z"]')
    sleep(1)
    ActionChains(chrome).click_and_hold()


