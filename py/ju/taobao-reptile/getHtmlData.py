import requests
from bs4 import BeautifulSoup
import json, re, demjson
from requests_html import HTMLSession, AsyncHTMLSession

headers = {
    "cookie": "t=8bc739d79ef4930d40cef60979578456; enc=AbSivTjEtV9USTxmuSGHR2bQd95SZA9LWNhTdaJPgvUsQOMf%2Fs9soin4pKXSCAEL2yaeVx6Nhl6%2BpeQHLtjOKQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; xlly_s=1; _samesite_flag_=true; cookie2=19834d517872ed3f1db562cd5b097c0c; _tb_token_=eb17d87573a54; cna=z2XMGGMVbRoCAXAuRv5JFOGI; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; dnk=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; mt=ci=69_1; sgcookie=E100XuyBg5k%2BlNxxd0JHO%2FfEFrio3z3XTrDzDm5x4OffUOdYIULWkbZtoSkg1ElGaibVrurNsxPflpHbv7ya7%2FX9Cw%3D%3D; unb=2283344656; uc1=cart_m=0&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie14=Uoe2zEMd8KKLGQ%3D%3D&pas=0&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQo9kR; uc3=id2=UUppqxL83am2iQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=0RIgGlUDxx5fJg%3D%3D&vt3=F8dCuw%2B%2FfI489QRmH7k%3D; csg=9c39e89f; cookie17=UUppqxL83am2iQ%3D%3D; skt=4759b75e7659ada7; existShop=MTYyMTQxMTk3NQ%3D%3D; uc4=nk4=0%400yrs34hrgOOnr%2BfuAYME3oM1pTdg&id4=0%40U2gjFQous65fn5OU84NxVNM6SA%2BP; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=%E9%B9%AB6f; _nk_=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; cookie1=WqSebVYTZljN%2FwGaIzCA6gdy1YVtCUq7YkPi1iE3QQQ%3D; _m_h5_tk=9663f2f325a9d4e1f510b1b4c2f80366_1621423278959; _m_h5_tk_enc=756f44d0e47f7e80386e7a8bee5b2229; isg=BIOD92CO506NRauKfIm6x9lnEkct-Bc6B6Tx6LVg3-JZdKOWPcinimHm6wQ6bm8y"
}
session = HTMLSession()
get = session.get(
    "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1621393357262_126&callback=jsonp127&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.439.9e0376524ns9SF&orderType=hotsell_desc&pageNo=3&tsearch=y",
    headers=headers)
# print(get.text)
html = None
items = []
itemIds = []

re_compile = re.compile(r'id=\d')


def jsonp127(str):
    soup = BeautifulSoup(str, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    print(type(find_all))
    for el in find_all:
        detail_url = el.attrs['href']
        items.append(detail_url)
        itemIds.append(re_compile.match(detail_url))

        # print(el.attrs['href'])
        # print(el.text)


eval(get.text)

print(items)

# 遍历List
# for itemUrl in items:
#     tempHeaders = {
#     "cookie": "t=8bc739d79ef4930d40cef60979578456; enc=AbSivTjEtV9USTxmuSGHR2bQd95SZA9LWNhTdaJPgvUsQOMf%2Fs9soin4pKXSCAEL2yaeVx6Nhl6%2BpeQHLtjOKQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; xlly_s=1; _samesite_flag_=true; cookie2=19834d517872ed3f1db562cd5b097c0c; _tb_token_=eb17d87573a54; cna=z2XMGGMVbRoCAXAuRv5JFOGI; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; dnk=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; mt=ci=69_1; sgcookie=E100XuyBg5k%2BlNxxd0JHO%2FfEFrio3z3XTrDzDm5x4OffUOdYIULWkbZtoSkg1ElGaibVrurNsxPflpHbv7ya7%2FX9Cw%3D%3D; unb=2283344656; uc1=cart_m=0&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie14=Uoe2zEMd8KKLGQ%3D%3D&pas=0&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&cookie21=WqG3DMC9Fb5mPLIQo9kR; uc3=id2=UUppqxL83am2iQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&nk2=0RIgGlUDxx5fJg%3D%3D&vt3=F8dCuw%2B%2FfI489QRmH7k%3D; csg=9c39e89f; cookie17=UUppqxL83am2iQ%3D%3D; skt=4759b75e7659ada7; existShop=MTYyMTQxMTk3NQ%3D%3D; uc4=nk4=0%400yrs34hrgOOnr%2BfuAYME3oM1pTdg&id4=0%40U2gjFQous65fn5OU84NxVNM6SA%2BP; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=%E9%B9%AB6f; _nk_=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; cookie1=WqSebVYTZljN%2FwGaIzCA6gdy1YVtCUq7YkPi1iE3QQQ%3D; _m_h5_tk=9663f2f325a9d4e1f510b1b4c2f80366_1621423278959; _m_h5_tk_enc=756f44d0e47f7e80386e7a8bee5b2229; isg=BIOD92CO506NRauKfIm6x9lnEkct-Bc6B6Tx6LVg3-JZdKOWPcinimHm6wQ6bm8y"
#     ,"referer":"https://detail.tmall.com/"
#     ,"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
#     }
#     session = HTMLSession()
#     itemDetail = session.get("https:" + itemUrl, headers=tempHeaders)
#     itemDetail.html.render()
#     find = itemDetail.html.find("#J_PromoPrice")
#     print(find)
#     print(itemDetail)

tempHeaders = {
    "cookie": "t=f433732176cf56fb2b5bc2d73cff325a; enc=5dbGo%2FN3O%2FcKL25XX0yuTgZDlQLAt0tVs1q4%2BOViYBKggX0Q9VnwAA4nEZChmdoKXf88vNkNtAatAONyOBNGyQ%3D%3D; _samesite_flag_=true; cookie2=121122a97f7d35ef482dedf6820a86a7; _tb_token_=3371ebb011e87; csg=9aee636d; skt=1b29338d3d2e674c; _cc_=WqG3DMC9EA%3D%3D; _m_h5_tk=6de3e730a0b3919b1dd17b6f4a4c1cee_1621056336268; _m_h5_tk_enc=7e4fad124038fb4aa5e331b6a09f13b9; cna=Qg30GPqC4z4CAXAuRv5eJZDx; uc1=cookie14=Uoe2zEf1b9l9Tg%3D%3D&cookie21=VT5L2FSpdiBh; isg=BE1NmEjIEbNNGbWZ4Tft7pU3XGnHKoH8GREb94_SieRThm04V3qRzJsX8BrgRpm0"
    ,"referer": "https://detail.tmall.com/item.htm?spm=a1z10.4-b-s.w19094187-15421479889.8.31676792iCNy9f&id=544875680495"
    ,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
url="https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId=596242155502&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621412968000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1621425094701&isg=eBIE8Mulj-IREsITBO5a-urza77t5IOXGSVzaNbMiInca6id1FMwrNCC2JVMRdtxgt5j1FKrjjACfRh95o4LRAkDBeYCKXIpBfpwoe1..&isg2=BF5e4ugwsi0flebJQjEjTjT6r_SgHyKZ4st8-wjmraG4K_IFda0FqQGKIjcnLhqx"
session_get = session.get(url, headers=tempHeaders)
print(session_get)
