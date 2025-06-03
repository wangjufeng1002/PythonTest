import json

import requests

request_temp = {
    "vhost": "/",
    "name": "material.modify.notice",
    "properties": {"delivery_mode": 2, "headers": {}, "content_type": "text/plain", "content_encoding": "UTF-8"},
    "routing_key": "",
    "delivery_mode": "2",
    "payload": "{\"optType\":\"AUDITED\",\"ids\":[\"3000-F00267\"]}",
    "headers": {},
    "props": {"content_type": "text/plain", "content_encoding": "UTF-8"},
    "payload_encoding": "string"
}


# 发送POST请求
def send_post_request(url, data=None, json=None, headers=None):
    response = requests.post(url, data=data, json=json, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def send_msg(exchange, routing_key, msg):
    url = "http://123.57.245.97:15673/api/exchanges/%2F/material.modify.notice/publish"
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "cookie": "m=2258:YWRtaW46dXc2c15UWVhrc1h3eXc%253D",
        "authorization": "Basic YWRtaW46dXc2c15UWVhrc1h3eXc="
    }
    request_temp["payload"] = msg
    request_temp["name"] = exchange
    request_temp["routing_key"] = routing_key

    reponse = send_post_request(url, json.dumps(request_temp, ensure_ascii=False), None, headers)
    return reponse


if __name__ == '__main__':
    send_msg(None, None, None)
