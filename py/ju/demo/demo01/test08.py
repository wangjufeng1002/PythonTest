# incoding=utf-8
# #名片管理系统
# 解释系统个菜单的功能
print("选项                      功能")
print("=" * 50)
print(" 0                       新增姓名")
print(" 1                       更改姓名")
print(" 2                       查询姓名")
print(" 3                       删除姓名")
print(" 4                     查询系统已录入的名字")
print(" 5                       退出系统")
print("=" * 50)

sourceInLines = ''
names = []

try:
    fileR = open("H://test.txt", 'r')
except IOError:
    fileW = open("H://test.txt", 'w')  # 创建文件
    fileW.close()
else:
    line = fileR.readline()
    while line:
        names.append(line.strip("\n"))
        line = fileR.readline()
    fileR.close()
fileA = open("H://test.txt", 'a')   # 追加文件
while True:
    # 提示用户输入选项
    num = input("请输入您的选项：")
    # 新增姓名
    if num == 0:
        name = input("请输入姓名：")
        names.append(name)
        for j in names:
            print(j)
            # 更改姓名
    elif num == 1:
        code = input("请输入您要更改的姓名的序号：")
        name = input("请输入正确的姓名：")
        names[int(code)] = name
        for j in names:
            print(j)
            # 查询姓名
    elif num == 2:
        name = input("请输入要查找的姓名：")
        if name in names:
            print ("系统中已经存在")
        else:
            print ("系统中不存在")
            # 删除姓名
    elif num == 3:
        name = input("请输入要删除的姓名：")
        names.reverse(name)
        for j in names:
            print j

            # 查询系统已录入的名字
    elif num == 4:
        print(" 序号        姓名")
        i = 0
        for name in names:
            print (" %d       %s " % (i, name))
        i += 1
    # 退出系统
    elif num == 5:
        for name in names:
            fileA.write(name)
            fileA.write('\n')
        fileA.close()
        break
    else:
        print("输入错误，请重新输入")
