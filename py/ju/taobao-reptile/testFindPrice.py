import json, re, demjson, time
file_url = open('D:\\爬虫\\TM\\detailHtml-test.txt', "r", encoding='utf-8')
readlines = file_url.readlines()
print(type(readlines))
itemId = re.match(".*?(id=.*&).*", readlines, re.S).group(1)


print(itemId)

