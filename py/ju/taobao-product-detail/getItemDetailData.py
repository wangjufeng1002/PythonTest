from bs4 import BeautifulSoup
import json, re, demjson
import time, random
from requests_html import HTMLSession, AsyncHTMLSession
import dataReptiledb
from entity import Book

# 从数据库获取的headers
# headers = dataReptiledb.getHeaders()
# 创建session
# session = HTMLSession()

# 代理 ip
# ip_list = ['218.249.45.162:52316', '123.118.0.27:8118', '114.249.115.204:9000', '106.14.198.6:8080',
#            '124.205.155.157:9090', '124.192.219.35:80', '106.14.198.6:8080', '103.233.154.242:8080',
#            '124.205.155.152:9090', '124.205.155.148:9090', '61.135.155.82:443']
# ip_list = dataReptiledb.getIpList()

# file_result = open('D:\\爬虫\\TM\\item-price.txt', "a+", encoding='utf-8')

# 促销 url
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false' \
               '&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false' \
               '&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621464441000&isRegionLevel' \
               '=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&casynSearchallback' \
               '=setMdskip&timestamp=1621491544699&isg=eBIE8Mulj-IREMTiBOfZhurza779OIRAguPzaNbMiOCPOefe' \
               '--xPW6s7QLTwCnGVh6YBJ3oiiBs_BeYBqgI-nxvOa6Fy_LDmn&isg2=BDo6VN' \
               '-xDhCfh4L9DsXP4jDGi2Bc677FZkeY70QzxU2DN9pxLXuv1QAGh8PrpzZd&ref=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm' \
               '%3Da1z10.3-b-s.w4011-23389038992.173.483f765292VfDy%26id%3D555824274521%26rn' \
               '%3D596ce34d3b21d41a4baf27d1cfaf0828%26abbucket%3D16'
promotionUrl = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621928176000&isRegionLevel=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&timestamp=1622029723119&isg=eBIE8Mulj-IREQ65BOfChurza779JIRYjuPzaNbMiOCP_Hf671mVW6sFIY8BCnGVh6AwJ3oiiBs_BeYBq_C-nxvOa6Fy_3Hmn&isg2=BPz8DUnnsCHnEoT3_AthiILwzZqu9aAfdLEeZdZ9POfMoZwr_wX0r_dQgcnZ0th3'


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')


def processPriceData(url, header, shopName, ipList):
    session = HTMLSession()
    detailResponse = session.get(url, headers=header, proxies={'http://': random.choice(ipList)})
    detailHtmlSoup = BeautifulSoup(detailResponse.text, features='html.parser')
    itemId = re.match(".*?(id=.*&).*", url, re.S).group(1).split('&')[0].replace('id=', '')
    itmDescUl = detailHtmlSoup.find_all(name="ul", attrs={"id": "J_AttrUL"})
    book = Book(tmId=itemId, name=None, isbn=None, auther=None, fixPrice=None, promotionPrice=None,
                promotionPriceDesc=None, price=None, promotionType=None, activeStartTime=None, activeEndTime=None,
                activeDesc="", shopName=shopName)
    contents = itmDescUl[0].contents
    for con in contents:
        if "书名" in con.next:
            book.setName(con.next.replace("书名: ", ""))
        if "ISBN" in con.next:
            book.setIsbn(con.next.replace("ISBN编号: ", ""))
        if ("作者" in con.next) or ("编者" in con.next):
            if "作者地区" not in con.next:
                book.setAuther(con.next.replace("作者: ", ""))
        if ("定价" in con.next) or ("价格" in con.next):
            book.setFixPrice(con.next.replace("定价: ", "").replace("价格: ", ""))
    promotionJsonp = session.get(promotionUrl.format(itemId=itemId), headers=header,
                                 proxies={'http://': random.choice(ipList)})
    promotionJSON = loads_jsonp(promotionJsonp.text)
    if promotionJSON.get("defaultModel") is None:
        print("{itemId} 获取不到促销信息啦，可能cookie失效".format(itemId=itemId))

    price = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def',{}).get('price')
    # 设置默认价格
    book.setPrice(price)
    # 促销列表
    promotionList = promotionJSON['defaultModel']['itemPriceResultDO']['priceInfo'].get('def',{}).get("promotionList", None)
    # 促销金额
    promotionPrice = 0
    promotionPriceType = ''
    if promotionList is None or len(promotionList) == 0:
        promotionPrice = 0
    else:
        promotionPrice = promotionList[0].get('price', 0)
        promotionPriceType = promotionList[0].get('type', "")
        promotionPriceDesc = promotionList[0].get('promText', "")
        startTime = promotionList[0].get("startTime")
        endTime = promotionList[0].get("endTime")
        # 设置促销价
        book.setPromotionPrice(promotionPrice)
        book.setPromotionType(promotionPriceType)
        book.setPromotionPriceDesc(promotionPriceDesc)
        book.setActiveStartTime(startTime)
        book.setActiveEndTime(endTime)

    # book.setPromotionPriceDesc(promotionPriceDesc)
    # 活动
    tmallShopProm = promotionJSON['defaultModel']['itemPriceResultDO']['tmallShopProm']
    if len(tmallShopProm) != 0:
        promPlanMsg = []
        for shopProm in tmallShopProm:
            promPlanMsg.append(",".join(shopProm['promPlanMsg']))
        book.setActiveDesc(promPlanMsg)
    # 写入文件
    dataReptiledb.insertDetailPrice(book)
    # file_result.write(book.toString() + '\n')
    # file_result.flush()
    print("process {id}".format(id=itemId))
    time.sleep(random.randint(2, 10))
    # time.sleep(random.randint(10, 20))


def getUrlDetailUrlFromFile():
    # headers 游标
    headersIndex = 0
    headers = dataReptiledb.getHeaders()
    ip_list = dataReptiledb.getIpList()

    file_url = open('D:\\爬虫\\TM\\item-detail-url.txt', "r", encoding='utf-8')
    item_urls = file_url.readlines()
    errorCnt = 0
    for i in range(len(item_urls)):
        url = item_urls[i]
        if "==" in url:
            continue
        try:
            processPriceData(url=url, header=headers[headersIndex], shopName="新华文轩网络书店", ipList=ip_list)
            i += 1
        except Exception as e:
            errorCnt += 1
            print("发生了点异常", e)
            if headersIndex == len(headers) - 1:
                headers = dataReptiledb.getHeaders()
                headersIndex = 0
            else:
                headersIndex += 1
            if errorCnt <= 20:
                i += 1
        # else:
        # dataReptiledb.updateSuccessFlag(1,)


def getUrlDetailUrlFromDB():
    # headers 游标
    headersIndex = 0
    # 获取数据库中的 headers
    headers = dataReptiledb.getHeaders()
    # 获取代理ip
    ipList = dataReptiledb.getIpList()
    # 获取url
    page = 1
    pageSize = 1000
    errorCnt = 0
    while True:
        print("处理第%d页数据" % page)
        item_urls = dataReptiledb.getItemUrl(page, pageSize)
        if item_urls is None:
            break
        else:
            i = 0
            while i < len(item_urls) - 1:
                url = item_urls[i]
                if url is None:
                    continue
                try:
                    processPriceData(url.itemUrl, headers[headersIndex], url.shopName, ipList=ipList)
                    i += 1
                except Exception as e:
                    errorCnt += 1
                    print("发生了点异常", e)
                    if headersIndex == len(headers) - 1:
                        headers = dataReptiledb.getHeaders()
                        headersIndex = 0
                    else:
                        headersIndex += 1
                    if errorCnt >= 20:
                        errorCnt = 0
                        i += 1
                        dataReptiledb.updateSuccessFlag(2, url.itemId)
                else:
                    dataReptiledb.updateSuccessFlag(1, url.itemId)
        page += 1


getUrlDetailUrlFromDB()
