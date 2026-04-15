import requests
import json
from toollib.guid import SnowFlake
snow = SnowFlake()

def send_post_request(url, data):
    headers = {
        "Content-Type": "application/json",
        "authorization": "Basic YWRtaW46dXc2c15UWVhrc1h3eXc="
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")


# 替换为目标 URL
target_url = "http://123.57.245.97:15673/api/exchanges/%2F/amq.default/publish"
# 基本的 JSON 模板
base_payload = {
    "vhost": "/",
    "name": "amq.default",
    "properties": {
        "delivery_mode": 1,
        "headers": {

        },
        "content_type": "text/plain",
        "content_encoding": "utf-8"
    },
    "routing_key": "mes-pms_equipment_modify_notify_exchange",
    "delivery_mode": "1",
    "headers": {

    },
    "props": {
        "content_type": "text/plain",
        "content_encoding": "utf-8"
    },
    "payload_encoding": "string"
}

target_url_2 = "http://123.57.245.97:15673/api/exchanges/%2F/mes-pms_equipment_modify_notify_exchange/publish"
base_payload_2 = {"vhost": "/", "name": "mes-pms_equipment_modify_notify_exchange",
                  "properties": {"delivery_mode": 2, "headers": {}, "content_type": "text/plain",
                                 "content_encoding": "UTF-8"}, "routing_key": "", "delivery_mode": "2",
                  "payload": "", "headers": {}, "props": {"content_type": "text/plain", "content_encoding": "UTF-8"},
                  "payload_encoding": "string"}

# 计划单列表
planOrderIds = ["1860116803047919616", "1861596117768970240"]

# def main():
#     # 循环发送请求
#     for code in planOrderIds:
#         # 更新 payload 中的 payload消息体
#         payload = base_payload.copy()
#         payload["payload"] = json.dumps({"planOrderId": code})
#
#         print(f"Sending payload for code: {code}")
#         send_post_request(target_url, payload)
# file_path = 'D:\\项目相关\\\mould\\equipment_change.txt'
# def main():
#     file = open(file_path, "r", encoding='utf-8')
#     line = file.readline()
#     while line:
#         if len(line) >0:
#             line = line[:-1]  # 去掉换
#             payload = base_payload_2.copy()
#             payload["payload"] = line
#
#             print(f"Sending payload for code: " + line);
#             send_post_request(target_url_2, payload)
#             print(line)
#             line = file.readline()
#
#     #更新 payload 中的 payload消息体
codes = ['JBS-2-ZS-03',
         'JBS-2-ZS-05',
         'JBS-2-ZS-06',
         'JBS-2-ZS-07',
         'JBS-2-ZS-09',
         'JBS-2-ZS-50',
         'JBS-2-ZS-51',
         'JBS-2-ZS-52',
         'JBS-2-ZS-54',
         'JBS-2-ZS-55',
         'JBS-2-ZS-56',
         'JBS-2-ZS-57',
         'JBS-2-ZS-58',
         'JBS-2-ZS-69',
         'JBS-2-ZS-71',
         'JBS-2-ZS-72',
         'JBS-2-ZS-73',
         'JBS-2-ZS-74',
         'JBS-2-ZS-75',
         'JBS-2-ZS-76',
         'JBS-2-ZS-77',
         'JBS-2-ZS-78',
         'JBS-2-ZS-79']
def main():
    for code in codes:
        payload = base_payload_2.copy()
        msg_item = json.dumps({"equipmentCode": code, "msgId": str(snow.gen_uid())})
        payload["payload"] = msg_item
        print(f"Sending payload for code: " + code)
        send_post_request(target_url_2, payload)
        print(msg_item)

if __name__ == '__main__':
    main()
