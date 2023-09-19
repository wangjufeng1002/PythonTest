import random

from requests_html import HTMLSession, AsyncHTMLSession

if __name__ == '__main__':
    proxies = [
        {'http': "http://" + "4495:1111@110.166.231.99:23063", 'https': "https://" + "4495:1111@110.166.231.99:23063"},
        {'http': "http://" + "4495:1111@125.75.149.208:23064", 'https': "https://" + "4495:1111@125.75.149.208:23064"},
        {'http': "http://" + "4495:1111@42.101.13.103:23065", 'https': "https://" + "4495:1111@42.101.13.103:23065"},
        {'http': "http://" + "4495:1111@14.18.32.136:23070", 'https': "https://" + "4495:1111@14.18.32.136:23070"},
        {'http': "http://" + "4495:1111@42.101.36.228:23071", 'https': "https://" + "4495:1111@42.101.36.228:23071"},

    ]
    proxy = {'http': "http://" + "4495:1111@110.166.231.99:23063", 'https': "https://" + "4495:1111@110.166.231.99:23063"}
    url = "http://httpbin.org/ip"

    html_session = HTMLSession()
    detailResponse = html_session.get(url=url, proxies=proxy)
    print(detailResponse.text)