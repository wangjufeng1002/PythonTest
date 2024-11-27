import os
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import db_operation

dir = 'E:\\video\\xinpianchang\\wm'


def init_webdriver() -> webdriver:
    url_host = 'https://uvwwk5w5ub.xyz/'
    url = 'https://uvwwk5w5ub.xyz/km/index.html#/hot_sq?num=0'
    options = Options()
    # 开启无界面模式
    options.add_argument("--headless")
    # 可选项：禁用GPU，可以解决一些莫名的问题
    options.add_argument("--disable-gpu")
    # 保持浏览器不关闭
    options.add_experimental_option('detach', True)
    service = Service(executable_path=r'D:\software-install-pk\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(5)
    # 获取页面上所有的元素
    all_elements = driver.find_elements(By.XPATH, "//*")

    driver.find_element(By.CLASS_NAME, "span2").click()
    time.sleep(5)
    # 获取页面源代码
    page_source = driver.page_source
    # 打印页面源代码
    print(page_source)

    return driver


def add_header_to_retrieve():
    headers = ('User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)
    return


def report_hook(blocks_read, block_size, total_size):
    if blocks_read * block_size >= total_size:
        print("Download finish")
    # if not blocks_read:
    #     print('Downloading: 0 Bytes')
    #     return
    # if total_size < 0:
    #     print('Downloading: %d Bytes' % (blocks_read * block_size))
    # else:
    #     print('Downloading: %d Bytes of %d' % (blocks_read * block_size, total_size))


def download_detail(web_driver: webdriver):
    cell_items = web_driver.find_elements(By.CLASS_NAME, "cell-item")
    for item in cell_items:
        try:
            img = item.find_element(By.TAG_NAME, 'img')
            record_key = img.get_attribute("data-src")
            records = db_operation.get_record(record_key)
            if len(records) > 0:
                print(record_key + " already exist in db")
                continue
            try:
                item.click()
                time.sleep(1)
                video = skip_detail(web_driver)
            except Exception as e:
                web_driver.save_screenshot("error.png")
                continue

            if video is None:
                web_driver.back()
                continue

            video_src = video.get_attribute("src")
            print(video_src)
            add_header_to_retrieve()
            file_name = video_src.split("/")[-1]
            urllib.request.urlretrieve(video_src, reporthook=report_hook, filename=dir + '\\' + file_name)

            # 记录日志
            db_operation.add_record(record_key, video_src, file_name)

            web_driver.back()
        except Exception as e:
            print(e)
            web_driver.save_screenshot("error.png")
            raise e

    web_driver.execute_script("window.scrollBy(0, -1000);")
    print("滑动一次")
    time.sleep(5)
    download_detail(web_driver)


def skip_detail(web_driver):
    video = web_driver.find_element(By.TAG_NAME, 'video')
    retry_count = 1
    while video is None and retry_count < 10:
        video = web_driver.find_element(By.TAG_NAME, 'video')
        time.sleep(1)
        retry_count += 1
    return video


if __name__ == '__main__':
    if os.path.exists(dir) is False:
        os.makedirs(dir)
    web_driver = init_webdriver()
    download_detail(web_driver)
