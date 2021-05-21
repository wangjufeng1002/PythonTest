import json, re, demjson
from bs4 import BeautifulSoup
import json, re, demjson
from requests_html import HTMLSession, AsyncHTMLSession

url = 'https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true&service3C=false' \
      '&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false&tryBeforeBuy=false&offlineShop=false' \
      '&itemId={itemId}&showShopProm=false&isPurchaseMallPage=false&itemGmtModified=1621464441000&isRegionLevel' \
      '=false&household=false&sellerPreview=false&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback' \
      '=setMdskip&timestamp=1621491544699&isg=eBIE8Mulj-IREMTiBOfZhurza779OIRAguPzaNbMiOCPOefe' \
      '--xPW6s7QLTwCnGVh6YBJ3oiiBs_BeYBqgI-nxvOa6Fy_LDmn&isg2=BDo6VN' \
      '-xDhCfh4L9DsXP4jDGi2Bc677FZkeY70QzxU2DN9pxLXuv1QAGh8PrpzZd&ref=https%3A%2F%2Fdetail.tmall.com%2Fitem.htm%3Fspm' \
      '%3Da1z10.3-b-s.w4011-23389038992.173.483f765292VfDy%26id%3D555824274521%26rn' \
      '%3D596ce34d3b21d41a4baf27d1cfaf0828%26abbucket%3D16'
session = HTMLSession()
tempHeaders = {
    "cookie":"t=8bc739d79ef4930d40cef60979578456; enc=AbSivTjEtV9USTxmuSGHR2bQd95SZA9LWNhTdaJPgvUsQOMf%2Fs9soin4pKXSCAEL2yaeVx6Nhl6%2BpeQHLtjOKQ%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=z2XMGGMVbRoCAXAuRv5JFOGI; lgc=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; tracknick=%5Cu6B8B%5Cu5FCD%5Cu7684%5Cu79C3%5Cu9E6B; mt=ci=69_1; uc3=nk2=0RIgGlUDxx5fJg%3D%3D&vt3=F8dCuw%2B%2FfIrB9q6hbi4%3D&id2=UUppqxL83am2iQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; sgcookie=E10072ym0tB5GwnGJXOSIKCFuPili3%2F7Jt0s8sWaxTHenGZvJM26Ubzr4hiOXAH8InP%2BHFs3QP7ymMYY%2BDBcJym%2F2Q%3D%3D; uc4=id4=0%40U2gjFQous65fn5OU84NxVNM%2BS%2BYm&nk4=0%400yrs34hrgOOnr%2BfuAYME3oMxDpG9; _cc_=UtASsssmfA%3D%3D; _samesite_flag_=true; cookie2=13d5b3109b190a26fc2db9f2add042cc; _tb_token_=3e18ee754e551; _m_h5_tk=e8cea713ed264ad59c93f3bb75e7f893_1621484810122; _m_h5_tk_enc=cee5d310a1b7c30b6c2263c7806c1ce4; uc1=cookie14=Uoe2zEMbjSBxZw%3D%3D; xlly_s=1; x5sec=7b226d616c6c64657461696c736b69703b32223a2236356437613838316435376634383366333330653832666337333338306135374350434e6d495547454a5379786f2b66794c756a5a7a443874736d4e41673d3d227d; isg=BNracF2tbnMGSeLtzdrDCPgEK4D8C17lhqd4D-RTmW04V3uRzJvk9UDmJyNLh9Z9",
    "referer": "https://detail.tmall.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
    except:
        raise ValueError('Invalid Input')


get = session.get(url, headers=tempHeaders)
jsonp = loads_jsonp(get.text)
print(jsonp)

