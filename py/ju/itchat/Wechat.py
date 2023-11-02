import itchat

if __name__ == '__main__':
    itchat.auto_login(hotReload=False)
    friends = itchat.get_friends(update=True)
    for item in friends:
        print(item['RemarkName'])