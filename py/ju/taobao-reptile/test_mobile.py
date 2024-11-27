import requests

if __name__ == '__main__':

    for i in range(0, 30):
        requests_get = requests.get("http://web.xi-9.com/apis/bigmall/oauth/code?mobile=15600611684")
        #requests_get = requests.get("https://web.xi-9.com/apis/uc/user/getCode?memberMobile=15600611684")
        print(requests_get.text)

    # post = requests.post("https://web.xi-9.com/apis/uc/user/getCode?memberMobile='1'")
    # print(post.text)