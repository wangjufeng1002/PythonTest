from py.ju.reptile.demo.entity import Data
import urllib.request
import base64
import re
import ssl
import translate
from translate import Translator

if __name__ == '__main__':
    s = "5LiL5LiA6aG1"
    print(base64.b64decode(s).decode('utf-8'))

    zh__translate= Translator(from_lang='ja', to_lang='zh').translate(base64.b64decode(s).decode('utf-8'))
    print(zh__translate)