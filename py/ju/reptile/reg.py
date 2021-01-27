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
    for math in matchObj:
        print(math)

else:
    print("No match!!")
