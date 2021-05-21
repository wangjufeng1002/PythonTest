#coding=utf-8
n=31
i=0
total=0
while i<31:
    if total >=200 :
        total +=5;
    elif total >= 150:
        total+=8;
    else:
        total+=10;
    i +=1;
print(total)
