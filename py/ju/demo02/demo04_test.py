# coding=UTF-8
print("你好")
print("欢迎进入名片管理系统！！！！")
print("-------------------------")
print("1: 添加用户")
print("2: 删除用户")
print("3: 修改用户")
print("4: 查找用户")
print("5: 显示菜单")
print("6: 退出系统")
print("7: 进入系统")
def showMenu():
    print("-------------------------")
    print("1: 添加用户")
    print("2: 删除用户")
    print("3: 修改用户")
    print("4: 查找用户")
    print("5: 显示菜单")
    print("6: 退出系统")
    print("7: 进入系统")
    print("-------------------------")
names=[]
def startSytem():
    while True:
        option = int(input("请输入您需要的操作:"))
        if option ==1:
            name = input("请输入要添加的姓名：")
            names.append(name)
            print("添加成功\n")
        elif option == 2:
            name = input("请输入要删除的姓名：")
            if(name in names):
                names.remove(name)
                print("删除成功")
            else:
                print("您要删除的姓名不在列表内")

showMenu()
startSytem()