import http
import requests
import hashlib


def md5_file(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            # 更新 MD5 对象
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def upload_file(file_path, url):
    file_md5 = md5_file(file_path)

    sign_md5 = hashlib.md5()
    sign_md5.update(file_md5.encode('utf-8'))
    sign_md5.update("3544b42263a1e48ce92e89792aef9ee0".encode("UTF-8"))
    sign = sign_md5.hexdigest()

    with open(file_path, 'rb') as f:
        files = {'file': f}
        headers = {"sign": sign}
        response = requests.post(url, files=files, headers=headers)
        print(response.status_code)
        print(response.text)


if __name__ == '__main__':
    url = "https://dmsstagegateway.jiabs.com/third/mes/equipment/uploadProcessParamFile/ZX01/"
    file_path = "D:\\项目相关\\MES2.0\\注塑机文档\\震雄\\参数文件\\MPC7-AiMld005.DAT"
    upload_file(file_path=file_path, url=url)
