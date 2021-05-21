import base64
import threading
from tkinter import Image
from selenium import webdriver
from time import sleep, time
import requests

session = requests.session()
verify_password_data='loginId=15091751738&password2=796b7308e7826d598a91bb78f229af550e3a3b7236868777dcf21355501dc22b7dee6e778082db4e99d08924fe8cb6ef232bb72de5a9085eeff9bd4626f5d8be0f9a4583d4c8e05e1c9101938a24d99645862ff59f31e869003ea55a0d9719936584061b774e8b22ecb21a44ed144bfb48d57afdc9a97cbcd71587ee1e0628dc&keepLogin=false&ua=140%23N71DPDz1zzPJ9zo2LZCTA6SoYboChuwwmSe4q1dhMIFRBDEoDXhFQ%2BCFo%2BXmbOy17oUnCsx80FIGNSjoYbZ96qWB2b9nlp1zz%2FlK1KW5TzzxzrPyOthqzFzb22U%2Bl61D9wzgUvILIzFd2PzvL6hqzFKhC2Y4lvzWrKwI1wba7XekT1LrGN1FzhZmDJXWLvIMGt7BaX38yRVNR5vmMrmlOAecnLQKdAWM2fP72rOp376DbYZ9WQ%2FNchPV1o9uR3iZSP2sS6IOcwp3Lg%2BFeK4JFB4QjQwKScKax4MQTEBziHDD8Ke4z%2BHTOypa5Vbro%2BoM5T4Rmx5iONHsaBk0RiomzEEXFWXXRGEol%2BNUGUPgSVi6De6tIHR5LA8BjkRwfIJVzwBO%2FDM%2BE%2FD%2FM2j%2B3qfxl6vH78Q3vbXUh%2FbwBLsnadY5FQiV%2F4h2Qo%2Bo4wnIcKEE%2Bz3hvKpJqhqTEzINdHjJ7Wm5opNuQn8AuaTdJMyJh4eEelwEfeKckRCWyFaNsRljZJVR6nymInv4YY6JuefL7q7xZCi7z7EXs60%2BfhM5j9o2tPJSv8aP1FhsU7PNSrtoZGgJ8%2FmYShIE46ksA2QU%2BRJ5SwDV3r0GwXzfLIeOZ04q2dQWcX27BgYU9dY%2BgDqWDDa5nMeFOGbdmXUbpSSU8MMzfvhn5xP7dCBljWsiOn%2Bw69m%2B4ivu5X2JjRidbeZJyjO5xECAY1yTwGbhB0TtLvw2XOC5Jmn58kT%2B3ezqvRkp3hkcSC14qU24xEdhJRDMMH5UidXm5U2cx%2BDRVy1n4pmF2i9Q6gEITxSN%2BpQPmrB2r1OZgEomODSBWpelPOfIMYchebRUsX%2FJmDzc3QAAtV7L3eWdeW1rafwQ6LFG5qNl1cpFjQkBtx9vyRFycssZ4Fh2neAD6BdMAAvrwsevY0NL0CVfaJnPWhFMXCafkxapJQTYzaZo%2F8VXzMJGY7oEcCB1XYJk4MAKNAGsYQLh38ZqpT%2F0AsmVAhzJW266A%2F8%2FPkODmjRlLtIuqRyMGAuASENNZzFr%2F1MI0kn1vvG8P9PKs2vzNSSofBpK7bwcOCvPuNVum1rufQNqhfL%2Bfi5Ke8YtR7xFAaPHto%2BOQKh7mpKv7F9WwJIqLYkoXfTBJAuvw1X6C943tz%3D%3D&umidGetStatusVal=255&screenPixel=1600x900&navlanguage=zh-CN&navUserAgent=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20WOW64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F90.0.4430.93%20Safari%2F537.36&navPlatform=Win32&appName=taobao&appEntrance=taobao_pc&_csrf_token=adOJ5zWitpDDWmxgXR43A1&umidToken=b0272f0d17cc9a04655c51a71c638c9b506756a7&hsiz=17a62963878c28d50816f129aa51d2a0&bizParams=&style=default&appkey=00000000&from=tb&isMobile=false&lang=zh_CN&returnUrl=http%3A%2F%2Fcart.taobao.com%2Fcart.htm%3Fspm%3Da220m.1000858.a2226mz.8.1b973daeyYZt2O%26from%3Dbtop&fromSite=0&bx-ua=211!qE4uf7pMUrA7UyEig78/C1Jkt1TPikGcPUyA+oI4BH9n7G/O85GKQx4h1jnf4axAWi62m4Mhqq5AE5NOuyfjO9k4ow+F9XXF5iuEUuHNLEPdUH3p7WI6QDkp6CsebmEb41/RKmZLJ1vR6fz9sF9kSPxcMJtAdTbSDmZBy8AIXZcuEPKdJRSIIcoHnkQyNWN6kUv2jFiy2WTKzcbRxT+NGQLLU8eaxrjP/AeIRfilm4u04kRgju9SbVKOw7BiCCpmRsBee2DL0Xn35QEHQm8GGqpWUUR56wFb+SB1YXyi2xGtocl+FIEEWihc7dmDSHpSTBNMGOe6QmkUcT11rp3L6s3wWf7ILQUbrbIs41qFF3omO4Zc0q5iIfHzrOR/TOpyk07AXC5Yl8U117BC/F8P3MQXHo0/QSQkTFoe952zsXjFL3SFn+2aGI8WlDbP8nlDLBD07bNEwYkyh4/6lk9bVrkqXvJIU6JXdqE4A7NEzEZ4xxNlr/guKCmLwwCyPG9TsVdEgsCY7Wjnf6Z1PhXp0m+EH9mFT1LbIkA8I+WlKxYRFNMrKCrZEQSIr2JG01tvj/Hqo/sWoHGhaDF3S9jBsqI1bgll4QE7at7x1jXQOVIsOI8ohD1O/v2Mt6jTy5czJZJnCeD1x7jeqMBRUA8EzcJpyPL9uGQTNIivLeG0BEAI4UxMT4jQvw+11t4aJuzxkwbl+GLb3JijnNXvXSjVn9rA3XqybYGqMR+RoCFlv+DDMmumH6tnxiBwL7OzH2RdSScjLFlsHMaihc5pWVj7TtIEd+nAllaudMXUMitDN4G2tR+MKBYO/I5+XCQG/NlSpM6imeLK13dC6/ZmZslX8o08ax/cfPi6ILh3RqNNqHxaGXXpt9i2EvXA6694ph5E7x/tH052kdq28bo5wyGIy9z176VkfF6GFLAc792UQvaY1rV6lm7U8G/u76EU779alnoy768uQvq+vBEO73NaUrso79MfggdLf88Ru9kFaHr4DSz5qV1YQ/t33Iki/lDrEg9hmob7OQ9cz9Gm4pDRMP6Dh+ezue3Ton8fklOsHnI6uYqLpJXGK2fIp0wGFiE+HI1S3U8MUVAsqRvTLTRmHJk6Lfxr57iB5HYP3mpX1Yll1bWOwSlCO0dCp0E6+0p2ZlVmG/VSjnjrskd0MFmEEJXi17W6GWCVL8wLydCaYCBOt/A9lhOE+R+kwFUnPToE7iqNkDz/lpI/bPgAWThQCyfANhoooMkPOZbmqfKoUrgPyKMxmjeip7flS3tkSX6NTopupldWlBRlp6y84RE9OFpz4D4EVSv5JPns8MVNXIv64MzilVBMl1QYx2saIGxCa0nLgvYgelDidt/9GKVM9fr7zIonJ7K3xwd2G7raOsUl6lefEOrL65gw0M41Jw/g8XQIBpl87kDC81ipAMc7llZF+xAOlO1+c+TLHMpX0EWUxFsAWQHhzWKfNTF45qieBiBsnjRpbGETxfHecrQWbpeYfh8yhIjA/PkWNa+xMKWYzXhWTW/fA4ODd4zDBpq6/LtJzmk28OV7FjyBssPll3uf6dN1JwSNd4QB89HUBrrPchtiIp+v+vOmNTrhLN5HD2rXJyFzOB4UeNZep7HEd8ECQHaK13NIt1iF2QxWtTGHzz8o/g7ps2cy6weFy9qRKk10YTZNkgGQPcgdkWLztPBz8KfRdpkqoJ4MPlZTPzdrfaCDW702iY75NjydqdKQ3FcjN3Gex55ZvABk00BXQbRt6ZkzBe/HB7P4rOgc4h/TyQTEFgZhxh5Q9jUeV0W/kuhap2g9zeZ/iwFh+c/k1WXGmZkQKHgQBscfnOn6Nb/CKqxE3YFf5l9zdKfT2WW/no/bJ2qV8ESS386I3BqGSPYgLkW8NHigJ7==&bx-umidtoken=T2gAFv77bn9XW80uKO8IHCRu3INnCXwmeAZ3sw30ccmybcGsClvFR0rLJ2YERB76Rhc=';
verify_password_headers = {
    # ':authority:': 'login.taobao.com',
    # ':method': 'POST',
    # ':path': '/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.31',
    # ':scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',

    'content-lengt': '3788',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'XSRF-TOKEN=781d165d-fe0a-4c08-9bc2-ca37d02286d3; _samesite_flag_=true; cookie2=17a62963878c28d50816f129aa51d2a0; t=e379a0bc1f5fbffc2f5c7a3a2c002e56; _tb_token_=e1119eab83abe; xlly_s=1; _bl_uid=Iyk8ao15jhRtzpjztqz7bvRrIRjw; thw=cn; enc=W8Sqkr0K0NyaHAWNqOGWup9z%2B3GRvszGQaztAyCBZMo0et1nxed%2BejPaVnOTndbCAdBqfLA9f5ekZ7bifY3l6w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=0feb754ba4d47d7999e41d1b8a1a551e_1620744099623; _m_h5_tk_enc=b493808cad676237a3f0603e5b85f016; mt=ci=0_0; tracknick=; cna=tTshGTH4EQUCAXAuRv6xRfic; l=eBT0GnRHj4kuXJQwBOfwourza77tcIRV_uPzaNbMiOCPO6fpSIGRW66wART9CnGVnsTv-35Z_VOzBc8S5yUIh6Yl3ZQ7XPQl6d8h.; isg=BCQkkg3xGA3NBWxBpXX3yEUZ9SIWvUgn_WHK3j5F2u-86cazZMlNt4UPqUFxNoB_; tfstk=cl6OBO9-dy4Muztd41F3hybbPsrhaDVpulTxHlOlskQ0VvMxhsxVETCWZftqWpEd.',
    'eagleeye-pappname': 'gf3el0xc6g@256d85bbd150cf1',
    'eagleeye-sessionid': '70ke1od0k7s0zjbjzokLz29s20qe',
    'eagleeye-traceid': 'c4729c521620735956238100150cf1',
    'origin': 'https://login.taobao.com',
    'referer': 'https://login.taobao.com/member/login.jhtml?spm=a21bo.21814703.754894437.1.5af911d9U4HRSf&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F',
   # 'sec-ch-ua': ' Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

post = session.post("https://login.taobao.com/newlogin/login.do?appName=taobao&fromSite=0&_bx-v=2.0.31",
                    headers=verify_password_headers, data=verify_password_data)
get = session.get(
    "https://list.tmall.com/search_shopitem.htm?spm=a220m.1000858.1000725.2.1b973daeyuyam6&user_id=101450072&from=_1_&stype=search")
print(post)
print(get)



