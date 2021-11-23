# https://www.btgw.xyz/download.php?class=guochan&id=7494427496567369
# https://www.btrs.xyz/html/movie/mobile/7064398583024740.html
# https://www.btrs.xyz/torrent/2806474170647561.torrent
import base64
import re
import urllib.request
import MyLog
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from entity import Data
import threading
import requests

log = MyLog.Logger("REP").get_log()

root_url = "aHR0cHM6Ly93d3cuYnRycy54eXo="
down = "aHR0cHM6Ly93d3cuYnRycy54eXovZG93bmxvYWQucGhwP2NsYXNzPWd1b2NoYW4maWQ9"
proxy_ip = {'http': "http://22925:4355@175.6.114.255:23052", 'https': "https://22925:4355@175.6.114.255:23052"}
header = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"
}


def process(page):
    global get, find_all
    proxy = {'http': "http://22925:4355@175.6.114.255:23052", 'https': "https://22925:4355@175.6.114.255:23052"}
    #
    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"
    }
    session = HTMLSession()
    try:
        get = session.get("https://www.btrs.xyz/list.php?class=guochan&page=" + str(page), headers=header, proxies=proxy_ip,
                          timeout=(5, 6))
        soup = BeautifulSoup(get.text, features='html.parser')
        find_all = soup.find_all(name="a", attrs={"target": "_blank"})
    except:
        log.error("deal with page {} list exception ".format(page))
        return []
    tag_ids = {}
    result = []
    for a in find_all:
        # dec = dec[0].replace('d(\'', '').replace('\'))', '')
        ids = re.findall(r'\d+', a.attrs['href'])
        if len(ids) != 1 or len(ids[0]) < 10:
            continue
        else:
            dec = ""
            date = a.previousSibling
            if len(a.contents) == 0:
                dec = ""
            else:
                try:
                    # region Description
                    dec = re.findall(r'd\(\'.*\)', a.contents[0].contents[0])
                    dec = dec[0].replace('d(\'', '').replace('\'))', '')
                    # endregion
                except:
                    pass
            result.append(Data(date=a.previousSibling, desc=dec, id=ids[0]))
    log.info("deal with page={} size={}".format(page, len(result)))
    return result


# path = "RDpcXHJlcGx0aWxlXFwlcy50b3JyZW50"
path = "L2Rldi9yZXB0aWxlL2RhdGEvJXMudG9ycmVudA=="


def search_down_url(result):
    proxy = urllib.request.ProxyHandler({'https': '22925:4355@175.6.114.255:23052'})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [("user-agent",
                          "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"
                          )]
    urllib.request.install_opener(opener)
    if len(result) <= 0:
        return
    session = HTMLSession()
    for data in result:
        url = base64.b64decode(down).decode("UTF-8") + data.id
        try:
            get = session.get(url, headers=header, proxies=proxy_ip, timeout=(5, 8))
            soup = BeautifulSoup(get.text, features='html.parser')
            find_all = soup.find_all(name="a", text=base64.b64decode("54K55Ye75LiL6L2956eN5a2Q").decode('utf-8'))
        except:
            continue
        if len(find_all) != 1:
            continue
        else:
            href = find_all[0].attrs['href']
            desc = data.desc
            retry = 0
            while True:
                try:
                    if desc is None or desc == '':
                        urllib.request.urlretrieve(base64.b64decode(root_url).decode("utf-8") + href,
                                                   base64.b64decode(path).decode("utf-8") % (str(data.id)))
                        break
                    else:
                        urllib.request.urlretrieve(base64.b64decode(root_url).decode("utf-8") + href,
                                                   base64.b64decode(path).decode("utf-8") % (getFileName(data)))
                        break
                except:
                    log.error("deal with  download exception")
                    retry += 1
                    if retry > 5:
                        break
                    pass

def getFileName(value):
    filename = base64.b64decode(value.desc).decode('utf-8')
    filename = filename.replace("\"", "&")
    filename = filename.replace("\'", "&")
    filename = filename.replace("\n", "&")
    filename = filename.replace(".", "")
    filename = filename.replace("1080P<font color=&blue&>[1080p]</font>", "")
    filename = filename.replace("<font color=&blue&>[1080p]</font>", "")
    filename = value.date + "&" + "(" + filename + ")"
    return filename


def test():
    proxy = {'http': "http://22925:4355@175.6.114.255:23052", 'https': "https://22925:4355@175.6.114.255:23052"}
    #
    header = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Mobile Safari/537.36"
    }
    session = HTMLSession()
    get = session.get("https://www.btgw.xyz/download.php?class=guochan&id=7494427496567369", headers=header,
                      proxies=proxy,
                      timeout=(3, 4))
    print(get)


def thread_exe(start, end):
    # while start < end:
    #     log.info("deal with page={}".format(start))
    #     ids = process(start)
    #     search_down_url(ids)
    #     start+=1
    while end > start:
        log.info("deal with page={}".format(end))
        ids = process(end)
        search_down_url(ids)
        end -= 1


if __name__ == '__main__':
    # limit = 100
    # index = 1
    # while index < 1001:
    #     thread = threading.Thread(target=thread_exe(index, index + limit, ))
    #     thread.start()
    #     index+=limit
    thread_1 = threading.Thread(target=thread_exe, args=(1, 472,))
    thread_2 = threading.Thread(target=thread_exe, args=(500, 987,))
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()

    # print(find_all)
    # test()

    # proxy = urllib.request.ProxyHandler({'https':'22925:4355@175.6.114.255:23052'})
    # opener = urllib.request.build_opener(proxy)
    # urllib.request.install_opener(opener)
    # urlopen = urllib.request.urlopen("http://httpbin.org/ip")
    # print(urlopen)
    # session = HTMLSession()
    # get = session.get("http://httpbin.org/ip", headers=header, proxies=proxy_ip, timeout=(3, 4))
    # print(get.text)
