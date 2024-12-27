import json

import requests

import settings
from RedisUtil import RedisTool

# 请替换为你的 AppID 和 AppSecret

APP_ID = settings.Config.APP_ID
APP_SECRET = settings.Config.APP_SECRET
WE_ACCESS_TOKEN = "WE_ACCESS_TOKEN"


# 获取 access_token
def get_access_token(app_id, app_secret):
    redis_tool = RedisTool().get_client()
    try:
        token = redis_tool.get(WE_ACCESS_TOKEN)
        if token:
            return token
        else:
            url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                token = result.get("access_token")
                print(f"获取微信 access-token 成功: {token}")
                redis_tool.setex(WE_ACCESS_TOKEN, 7000, token)
                return token
            else:
                print("获取 access_token 失败")
                return None
    except Exception as e:
        print(f"An redis error occurred: {e}")
        raise ValueError("对不起，由于当前访问量过高，当前提问已被限制，请重新提问，谢谢~")
    finally:
        redis_tool.close()

# 创建自定义菜单
def create_custom_menu(access_token, menu_data):
    url = f"https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(menu_data, ensure_ascii=False).encode("utf-8"))
    if response.status_code == 200:
        result = response.json()
        if result.get("errcode") == 0:
            print("创建自定义菜单成功")
        else:
            print(f"创建自定义菜单失败，错误码：{result.get('errcode')}，错误信息：{result.get('errmsg')}")
    else:
        print("创建自定义菜单失败")


# 删除自定义菜单
def delete_menu(access_token):
    url = f'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        if result['errcode'] == 0:
            print('删除自定义菜单成功')
        else:
            print('删除自定义菜单失败:', result)
    else:
        print('请求删除自定义菜单失败:', response.status_code)


def get_menu_data():
    menu_data = {
        "button": [
            {
                "type": "click",
                "name": "功能说明",
                "key": "reply_description"
            },
            {
                "name": "见面礼",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "ChatGPT学习手册",
                        "url": "https://ydyrb84oyc.feishu.cn/docx/CdGldIeJToqC2zxifLccDlAan7d"
                    },
                    {
                        "type": "view",
                        "name": "大模型APIKey && 三款免费的AI工具",
                        "url": "https://javastarboy.com/"
                    },
                    # {
                    #     "type": "miniprogram",
                    #     "name": "社群",
                    #     "url": "#小程序://知识星球/vE0yq6V9KNRuiln",
                    #     "appid": "wx286b93c14bbf93aa",
                    #     "pagepath": "pages/lunar/index"
                    # },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }]
            },
            {
                "name": "精选推荐",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "白嫖6款ChatGPT工具",
                        "url": "https://mp.weixin.qq.com/s/wR3o9Rj255bBabbm6hZKVA"
                    },
                    {
                        "type": "view",
                        "name": "ChatGPT提问技巧与案例",
                        "url": "https://mp.weixin.qq.com/s/vmGzhmc5L1VPKQ80c9Alfw"
                    },
                    {
                        "type": "view",
                        "name": "OpenAI开发之五种场景四个重点",
                        "url": "https://mp.weixin.qq.com/s/Dtv77Z5PKOBUB1w6sXUzEg"
                    },{
                        "type": "view",
                        "name": "公众号与网页版原理剖析",
                        "url": "https://mp.weixin.qq.com/s/CV6Vwa6GzpkeGHBfChw1_A"
                    }]
            }]
    }
    return menu_data


if __name__ == "__main__":
    access_token = get_access_token(APP_ID, APP_SECRET)
    print(f"access_token==={access_token}")
    if access_token:
        delete_menu(access_token)
        menu_data = get_menu_data()
        create_custom_menu(access_token, menu_data)
