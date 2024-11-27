import re

str = "<li>aaaa</li>"
line = "Cats are smarter than dogs"
matchObj = re.match(r'(.*) are (.*?) .*', line, re.M | re.I)
if matchObj:
    print("matchObj.group() : ", matchObj.group())
    print("matchObj.group(1) : ", matchObj.group(1))
    print("matchObj.group(2) : ", matchObj.group(2))
else:
    print("No match!!")

matchObj = re.findall(r'(\<.*\>)', str, re.M | re.I)
if matchObj:
    for math in \
            matchObj:
        print(math)

else:
    print("No match!!")

if __name__ == '__main__':
    str = '''<li>[11-14] <a href="/html/movie/pc/7787479138933122.html" target='_blank'><script type="text/javascript">document.write(d('5b6I5ryC5Lqu55qE576O5aWz5Li75pKt6L+Y5Lya5LiA5a2X6amsIOWwuuW6puWkp+engOiHquaFsCDov5npgLzmr5vmnInngrnlpJo='));</script></a></li>
    '''
    uri = re.findall(r'href="/html/movie/pc/\d*.html"', str)
    print(uri)
