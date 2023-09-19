import os

if __name__ == '__main__':
    dir = 'E:\\电子书\\rep'
    listdir = os.listdir(dir)
    for file in listdir:
        if '' in file:
            print(file)
