import requests
from tqdm import tqdm
import json
import os
import hashlib

# 收藏夹请求头
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Referer": "https://www.douyin.com/user/self?from_tab_name=main&showTab=favorite_collection",
    "Cookie": "LOGIN_STATUS=1; store-region=cn-sn; store-region-src=uid; bd_ticket_guard_client_web_domain=2; xgplayer_user_id=469068096952; passport_assist_user=Cj3qY1BVGt9m4M_vYQeFg3S9xXqHP7o3zScAcmmrJEUVqV1KK5yOg7ihVmvVD3C70_YleTKv49m4KYXtZFE3GkoKPIMLuGtq1-PMkuWPu5WHHYnIvz3IUpc-ta8jhTnvUlR1UoZleoTT_bVaLxeXtDn0eDGGPkZ2DyBJfpBpiBDb9cUNGImv1lQgASIBA1Z8NgM%3D; uid_tt=9fb2cd44971ea9b5261717cf0ade4411; uid_tt_ss=9fb2cd44971ea9b5261717cf0ade4411; sid_tt=d2c891212b549b67444fc34719f8c4f3; sessionid=d2c891212b549b67444fc34719f8c4f3; sessionid_ss=d2c891212b549b67444fc34719f8c4f3; ttwid=1%7C4OSezhwsnRNVo_VvD3zhom5o6QVEBcVNbRfBLDnKcdM%7C1711761277%7Cf581354d57165089a5e6bcc72bc0978d4f8eb83fb638cbf10ba2b5ee325e54ec; SEARCH_RESULT_LIST_TYPE=%22single%22; __live_version__=%221.1.1.9930%22; live_use_vvc=%22false%22; UIFID_TEMP=3451f3290245f54d68444d1ea9b086549aa1429a8a34f8bce366bfaafc2ae532a9385b89e83d55c5cc9c0b478b59617d870fb92fc692c83f080ccb03d64bda2f3e4928a50dea01139ff7a83d35e504e1; fpk1=U2FsdGVkX1+QTkhQlXzgQg5BzZjOBhvXy8w4CX6usAFYFfV1AOvw19kctfn16CywT8qC5SwKL6ILTdz0MOUn5g==; fpk2=5e705226acd7a97aa6ee95ab188632d6; UIFID=3451f3290245f54d68444d1ea9b086549aa1429a8a34f8bce366bfaafc2ae532a9385b89e83d55c5cc9c0b478b59617d71504ae459adb8a2dcada1e71d98b5489bdf800664e21b69c1a859e6edb5ad7aeb30023c116f7e0ca09f5609bff7ae914931a730463e69aaea5749926c38988bd20aebab8a8a097a70f71719fe7bb86a1bef808419befc9004c167110c4e50d59f33f54ee12518da607de4bb3e89af76; my_rd=2; __ac_nonce=066e12e9b00c92784fcbb; __ac_signature=_02B4Z6wo00f01EkUHWQAAIDBm3llpU5CfohJNBnAAHSr08dSMX6dc0ZyIcsQFL8EIa6tQlknLaF3ylFKreDP1FFDkjnztttecESFBl1GS6J4Z6SEooYAFDr8hh.6BOrKs.htuM21.rkfVdv-54; csrf_session_id=a508aa5948bb94fce135ebe4948d7616; s_v_web_id=verify_m0xftnxf_k3yMxqdM_lYoO_4DLo_8Qk5_BH3Rld9eTJXD; strategyABtestKey=%221726033572.211%22; biz_trace_id=f9c2c354; passport_csrf_token=c8b45d358f1e5522d0e0277f021d3d73; passport_csrf_token_default=c8b45d358f1e5522d0e0277f021d3d73; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.226%7D; publish_badge_show_info=%220%2C0%2C0%2C1726033573691%22; is_staff_user=false; pwa2=%220%7C0%7C1%7C0%22; passport_mfa_token=CjVnT4zp4oBLZ%2B%2B7ejOWpfL05eXwf6pqYmOJeO6Fu9usB9Qc8XGheHJcqt2pdaBQ7tzTQYwORBpKCjxbfaPiwL5ptFoZa0RxTSK2%2FC6IgpMliCgB7n9ry0MpLaj3U%2Bz%2BP4aar47RD3gOAqE4Uqc6EnFrt14wd3MQ%2FebbDRj2sdFsIAIiAQP4tMOT; d_ticket=d04eda3cabaf67671fecef7a3d6d380246b28; sid_guard=d2c891212b549b67444fc34719f8c4f3%7C1726033630%7C5183938%7CSun%2C+10-Nov-2024+05%3A46%3A08+GMT; sid_ucp_v1=1.0.0-KGMzNjhiZTA1YzViNDgwOGU0MWI3NmZjZGZlZWNlMTYxOWY4NjllMjcKHwjN0J6z9QIQ3t2EtwYY7zEgDDDE14TZBTgGQPQHSAQaAmhsIiBkMmM4OTEyMTJiNTQ5YjY3NDQ0ZmMzNDcxOWY4YzRmMw; ssid_ucp_v1=1.0.0-KGMzNjhiZTA1YzViNDgwOGU0MWI3NmZjZGZlZWNlMTYxOWY4NjllMjcKHwjN0J6z9QIQ3t2EtwYY7zEgDDDE14TZBTgGQPQHSAQaAmhsIiBkMmM4OTEyMTJiNTQ5YjY3NDQ0ZmMzNDcxOWY4YzRmMw; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=1edaf9ab2b571abadd83ff1f5f31e10d; __security_server_data_status=1; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAA8P9NTFFLm9fr4bIY4aFO_eFWjD6VJoeUI_rLTmps8OU%2F1726070400000%2F0%2F1726033765467%2F0%22; WallpaperGuide=%7B%22showTime%22%3A1726033710281%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A25%2C%22cursor2%22%3A4%7D; download_guide=%223%2F20240911%2F0%22; _tea_utm_cache_1243=undefined; MONITOR_WEB_ID=4d5da3b9-164f-4aa9-b6bb-8d971d2a17cf; douyin.com; xg_device_score=7.4739383192298945; device_web_cpu_core=12; device_web_memory_size=8; architecture=amd64; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A1%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; IsDouyinActive=true; dy_swidth=794; dy_sheight=774; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A794%2C%5C%22screen_height%5C%22%3A774%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRUpTWXJidTJhZXdJbHBLeHEwZlZNazV3VnJBVGRvQXd5ejRsS3d5WXZySFpzYVM2UjNuZXhVL2NpZG53MGJQTXJnRkJNNmNZemNuYitaUjdKWm4wbG89IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; passport_fe_beating_status=true; home_can_add_dy_2_desktop=%221%22; odin_tt=8d30cb3215e5f6c60af69829404c4c9db4903c0dd7266296f2e87805339aa57307a9d6fb5d1a50bdc3193b8f5240aed6b3668d37d3a90fafe87181172315a0d7; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAA8P9NTFFLm9fr4bIY4aFO_eFWjD6VJoeUI_rLTmps8OU%2F1726070400000%2F0%2F1726034371508%2F0%22"
}
# 收藏夹id
collects_id = 7413259558992434953
# 指针
cursor = 0
# 收藏夹url
url = 'https://www.douyin.com/aweme/v1/web/collects/video/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&collects_id={collects_id}&cursor={cursor}'
# 收藏夹

images = []


# 处理数据
def Data():
    # 指针
    cursor = 0
    # 意味着 最多扫描 10*30 个视频
    for i in range(10):
        _url = url.format(collects_id=collects_id, cursor=cursor)
        dy_rs = requests.get(url=_url, headers=header)
        if dy_rs.json()['aweme_list'] is None or dy_rs.ok is False:
            return
        else:
            getUrl(dy_rs.json())
            cursor += 30


# 获取视频/图片url
def getUrl(res_json):
    for video in tqdm(res_json['aweme_list'], desc='获取视频/图片url'):
        # print(json.dumps(video, sort_keys=True, indent=2))
        # 获取作者 name
        author = video['author']['nickname']
        # 获取文案
        # ptitle = video['desc']
        if video.get('images'):  # 图文类型
            for img in video['images']:
                images.append({"author": author, "type": "jpg", "uri": img['uri'], "url": img['url_list'][0]})
        elif video.get('video'):  # 视频类型
            # 视频url
            images.append({"author": author, "type": "mp4", "uri": video['video']['play_addr_h264']['uri'],
                           "url": video['video']['play_addr_h264']['url_list'][0]})
            # 封面图片url
            images.append({"author": author, "type": "jpg", "uri": video['video']['cover']['uri'],
                           "url": video['video']['cover']['url_list'][1]})


# 下载图片和视频
def download_media(images):
    if len(images) == 0:
        print("未获取到 视频url")
        return
    # 创建抖音收藏夹下载文件夹 在脚本当前目录
    if not os.path.exists('抖音收藏夹下载'):
        os.makedirs('抖音收藏夹下载')

    for im in tqdm(images, desc='正在下载'):
        # 创建 博主文件夹，存放同个博主的内容
        if not os.path.exists(f'抖音收藏夹下载/{im["author"]}'):
            os.makedirs(f'抖音收藏夹下载/{im["author"]}')
            open(f'抖音收藏夹下载/{im["author"]}/log.txt', "w").close()

        # 判断 当前url是否已经下载过
        downloaded = False
        md5 = f'{get_md5(im["uri"])}\n'
        with open(f'抖音收藏夹下载/{im["author"]}/log.txt', 'r', encoding='utf-8') as f:
            file_lines = f.readlines()
        for _md5 in file_lines:
            if _md5 == md5:
                downloaded = True
                break

        # 如果没下载过则下载
        if not downloaded:
            num_png = len(os.listdir(f'抖音收藏夹下载/{im["author"]}'))
            img_req = requests.get(url=im["url"]).content
            with open(f'抖音收藏夹下载/{im["author"]}/{num_png}.{im["type"]}', 'wb') as f:
                f.write(img_req)
            with open(f'抖音收藏夹下载/{im["author"]}/log.txt', 'a', encoding='utf-8') as f:
                f.write(f'{md5}\n')


def get_md5(url):
    # 因为python3运行内存中编码方式为unicode，所以将url md5压缩之前首先需要编码为utf8。
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


Data()
download_media(images)
