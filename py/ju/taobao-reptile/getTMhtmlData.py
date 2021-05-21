
from bs4 import BeautifulSoup
import json, re, demjson, time
from requests_html import HTMLSession, AsyncHTMLSession
from entity import Book
import random

# tempHeaders = {
#     "cookie": "t=f433732176cf56fb2b5bc2d73cff325a; enc=5dbGo%2FN3O%2FcKL25XX0yuTgZDlQLAt0tVs1q4%2BOViYBKggX0Q9VnwAA4nEZChmdoKXf88vNkNtAatAONyOBNGyQ%3D%3D; _samesite_flag_=true; cookie2=121122a97f7d35ef482dedf6820a86a7; _tb_token_=3371ebb011e87; csg=9aee636d; skt=1b29338d3d2e674c; _cc_=WqG3DMC9EA%3D%3D; _m_h5_tk=6de3e730a0b3919b1dd17b6f4a4c1cee_1621056336268; _m_h5_tk_enc=7e4fad124038fb4aa5e331b6a09f13b9; cna=Qg30GPqC4z4CAXAuRv5eJZDx; uc1=cookie14=Uoe2zEf1b9l9Tg%3D%3D&cookie21=VT5L2FSpdiBh; isg=BE1NmEjIEbNNGbWZ4Tft7pU3XGnHKoH8GREb94_SieRThm04V3qRzJsX8BrgRpm0"
#     ,
#     "referer": "https://detail.tmall.com/item.htm?spm=a1z10.4-b-s.w19094187-15421479889.8.31676792iCNy9f&id=544875680495"
#     ,
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
# }
tempHeaders = {
    "cookie": "cna=su4sGQKI/EsCAXAuRv6SBDbi; xlly_s=1; cq=ccp%3D1; dnk=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0&existShop=false&cookie21=VT5L2FSpccLuJBreK%2BBd&cookie14=Uoe2zEMVbp%2Fh%2Bw%3D%3D; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dCuw%2B%2FdPVILH3uaRg%3D&nk2=0RIgGlUDxx5fJg%3D%3D&id2=UUppqxL83am2iQ%3D%3D; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; lid=%E6%AE%8B%E5%BF%8D%E7%9A%84%E7%A7%83%E9%B9%AB; uc4=nk4=0%400yrs34hrgOOnr%2BfuAYME3ouN%2FgOO&id4=0%40U2gjFQous65fn5OU84NxVNvry5iG; _l_g_=Ug%3D%3D; unb=2283344656; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; cookie1=WqSebVYTZljN%2FwGaIzCA6gdy1YVtCUq7YkPi1iE3QQQ%3D; login=true; cookie17=UUppqxL83am2iQ%3D%3D; cookie2=18bdf90068c6e12161639e76bd4124ba; _nk_=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; sgcookie=E100yPtCKfqNCDwyeD8dLjNkUTCtz2NsCjmGlQnrFUUXifHHih2TXy4MK5iqD%2Fc5wx%2FdWXxuI5ByuRNcwWWe3dSeWg%3D%3D; t=2052357122849a2343cf8f3414a98a23; sg=%E9%B9%AB6f; csg=c763d8fe; _tb_token_=36835b9be7ebe; pnm_cku822=; enc=amin6PIbqHhE8PS40Fne%2B7YyCo2FMxE7fLO%2BHMCZHgvSOBofXWSKNlT3of2GZWFy8y7upxnJ8hBw57u8t%2BlldA%3D%3D; l=eBr5IkElj62nJEZaBOfwourza77OSIRAguPzaNbMiOCPOw5p5g2CW6sP4oL9C3GVh682R3oiiBs_BeYBqIjOov33l6m9q3Dmn; isg=BOvrvx37D5RpqVNATe_3K-JPeg_VAP-CLzxpsF1oxyqB_Ate5dCP0olaVjySXFd6; tfstk=caS1B7AS9fcsfCUqbOwE7gOAuPxfZ3UBpPOFCaI9IqVbkQX1itiyNpkGoXipyp1..",
    "referer": "https://winshare.tmall.com/search.htm?spm=a1z10.5-b-s.0.0.72fb2491fdaM8a&search=y&orderType=defaultSort",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
url = "https://winshare.tmall.com/i/asynSearch.htm?_ksTS=1621492071157_128&callback=jsonp&mid=w-23389038992-0&wid=23389038992&path=/search.htm&search=y&spm=a1z10.3-b-s.w4011-23389038992.442.a51776523QlLqc&orderType=defaultSort&pageNo={pageNo}&tsearch=y"

promotionHeaders = {
    "cookie":"t=8bc739d79ef4930d40cef60979578456; enc=AbSivTjEtV9USTxmuSGHR2bQd95SZA9LWNhTdaJPgvUsQOMf%2Fs9soin4pKXSCAEL2yaeVx6Nhl6%2BpeQHLtjOKQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=z2XMGGMVbRoCAXAuRv5JFOGI; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; mt=ci=69_1; uc3=nk2=0RIgGlUDxx5fJg%3D%3D&vt3=F8dCuw%2B%2FfIrB9q6hbi4%3D&id2=UUppqxL83am2iQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; sgcookie=E10072ym0tB5GwnGJXOSIKCFuPili3%2F7Jt0s8sWaxTHenGZvJM26Ubzr4hiOXAH8InP%2BHFs3QP7ymMYY%2BDBcJym%2F2Q%3D%3D; uc4=id4=0%40U2gjFQous65fn5OU84NxVNM%2BS%2BYm&nk4=0%400yrs34hrgOOnr%2BfuAYME3oMxDpG9; _cc_=UtASsssmfA%3D%3D; _samesite_flag_=true; cookie2=13d5b3109b190a26fc2db9f2add042cc; _tb_token_=3e18ee754e551; _m_h5_tk=e8cea713ed264ad59c93f3bb75e7f893_1621484810122; _m_h5_tk_enc=cee5d310a1b7c30b6c2263c7806c1ce4; uc1=cookie14=Uoe2zEMbjSBxZw%3D%3D; xlly_s=1; x5sec=7b226d616c6c64657461696c736b69703b32223a22346432393137376631383134373535316262373762313961343263636435323143504c6b6d495547454937557450444531756e344e54443874736d4e41673d3d227d; isg=BCQkkvRfGDGI6mxPNywVCvIa9SIWvUgnXMl27T5F---y6cWzZs1Wt4MIqEFxF4B_",
    "referer": "https://detail.tmall.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",

}
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false' \
               '&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false' \
               '&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621464441000&isRegionLevel' \
               '=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback' \
               '=setMdskip&timestamp=1621491544699&isg=eBIE8Mulj-IREMTiBOfZhurza779OIRAguPzaNbMiOCPOefe' \
               '--xPW6s7QLTwCnGVh6YBJ3oiiBs_BeYBqgI-nxvOa6Fy_LDmn&isg2=BDo6VN' \
               '-xDhCfh4L9DsXP4jDGi2Bc677FZkeY70QzxU2DN9pxLXuv1QAGh8PrpzZd&ref=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm' \
               '%3Da1z10.3-b-s.w4011-23389038992.173.483f765292VfDy%26id%3D555824274521%26rn' \
               '%3D596ce34d3b21d41a4baf27d1cfaf0828%26abbucket%3D16'
session = HTMLSession()

books = []
file_object = open('C:\\Users\\wangjufeng\\Desktop\\tm-03.txt', "a", encoding='utf-8')


def jsonp(str):
    detailUrl = []
    soup = BeautifulSoup(str, features='html.parser')
    find_all = soup.find_all(name="a", attrs={"class": "J_TGoldData"})
    for el in find_all:
        detail_url = el.attrs['href']
        detailUrl.append(detail_url)

    return detailUrl


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def relatedAuctionsItem(relatedAuctionsItemIds):
    url = 'https://detail.tmall.com/item.htm?spm=a220o.1000855.0.da321h.6e8110aarO1G0Z&id={id}'
    for id in relatedAuctionsItemIds:
        detailHtml = session.get(url.format(id=id), headers=tempHeaders)
        detailHtmlSoup = BeautifulSoup(detailHtml.text, features='html.parser')
        itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})

        itemId = id
        ## 创建 book对象
        book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None, price=None, activeDesc=None)
        contents = itmDescUl[0].contents
        for con in contents:
            if "书名" in con.next:
                book.setName(con.next)
            if "ISBN" in con.next:
                book.setIsbn(con.next)
            if ("作者" in con.next) or ("编者" in con.next):
                book.setAuther(con.next)
            if ("定价" in con.next) or ("价格" in con.next):
                book.setPrice(con.next)
        # time.sleep(2)
        promotionJsonp = session.get(promotionUrl.format(itemId=itemId), headers=promotionHeaders)
        promotionJSON = loads_jsonp(promotionJsonp.text)
        # 促销列表
        promotionList = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo']['def']['promotionList']
        # 促销金额
        promotionPrice = 0
        if len(promotionList.length) == 0:
            promotionPrice = 0
        else:
            promotionPrice = promotionList[0]['price']
        book.setPromotionPrice(promotionPrice)
        books.append(book)
        file_object.write(book.toString())
        file_object.flush()
        time.sleep(random.randint(10, 20))


def dealData(detailUrl):
    for itemUrl in detailUrl:
        detailHtml = session.get("https:" + itemUrl, headers=tempHeaders)
        detailHtml.html.render()
        detailHtmlSoup = BeautifulSoup(detailHtml.text, features='html.parser')
        itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
        price = detailHtmlSoup.find(name="span", attrs={"class": "tm-price"})
        itemId = re.match(".*?(id=.*&).*", itemUrl, re.S).group(1).split('&')[0].replace('id=', '')
        ## 创建 book对象
        book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None ,promotionPrice=None, price=None, activeDesc="")
        contents = itmDescUl[0].contents
        for con in contents:
            if "书名" in con.next:
                book.setName(con.next)
            if "ISBN" in con.next:
                book.setIsbn(con.next)
            if ("作者" in con.next) or ("编者" in con.next):
                book.setAuther(con.next)
            if ("定价" in con.next) or ("价格" in con.next):
                book.setFixPrice(con.next)
        promotionJsonp = session.get(promotionUrl.format(itemId=itemId), headers=promotionHeaders)
        promotionJSON = loads_jsonp(promotionJsonp.text)
        # 促销列表
        promotionList = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo']['def']['promotionList']
        # 促销金额
        promotionPrice = 0
        if len(promotionList) == 0:
            promotionPrice = 0
        else:
            promotionPrice = promotionList[0]['price']
        # 设置促销价
        book.setPromotionPrice(promotionPrice)

        # 活动
        tmallShopProm = promotionJSON['defaultModel']['itemPriceResultDO']['tmallShopProm']
        if len(tmallShopProm) != 0:
            promPlanMsg = []
            for shopProm in tmallShopProm:
                promPlanMsg.append(",".join(shopProm['promPlanMsg']))
            book.setActiveDesc(promPlanMsg)
        books.append(book)
        # 写入文件
        file_object.write(book.toString() + '\n')
        file_object.flush()
        print("process {id}".format(id=itemId))
        time.sleep(random.randint(10, 20))
        # 其他版本
        # relatedAuctions = promotionJSON['defaultModel']['relatedAuctionsDO']['relatedAuctions']
        # relatedAuctionsItemIds = []
        # if len(relatedAuctions) != 0:
        #     for relatedAuction in relatedAuctions:
        #         relatedAuctionsItemIds.append(relatedAuction['itemId'])
        # if len(relatedAuctionsItemIds) != 0:
        #     print("还有一些没输出")
        # relatedAuctionsItem(relatedAuctionsItemIds)


for i in range(3, 100):
    print("开始抓取第 {page}页 {time}".format(page=i, time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    url_format = url.format(pageNo=i)
    listResult = session.get(url_format, headers=tempHeaders)
    detailUrl = eval(listResult.text)
    detailUrl = list(set(detailUrl))
    print("第 {page} 页需要处理 {num}条 {time}".format(page=i, num=len(detailUrl),
                                                time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    dealData(detailUrl)
    time.sleep(random.randint(5, 15))
    # print(url_format)
