import datetime
# 用您的 API 密钥替换以下字符串
import json
import requests

import settings

# 企业转发 url
baseTxProxyUrl = settings.Config.baseTxProxyTranspondUrl
subscription_url = baseTxProxyUrl + "/v1/dashboard/billing/subscription"


def getUsage(FromUserName, apikey):
    headers = {
        "Authorization": "Bearer " + apikey,
        "Content-Type": "application/json",
        "check": "1"
    }
    subscription_response = requests.get(subscription_url, headers=headers)
    if subscription_response.status_code == 200:
        data = subscription_response.json()
        # 订阅总额度
        total = data.get("hard_limit_usd")
        # 订阅有效期截止时间
        if data.get("access_until") != None:
            access_until = datetime.datetime.fromtimestamp(data.get("access_until"))
        else:
            access_until = '9999-12-31'
    else:
        try:
            response_dict = json.loads(subscription_response.text)
            if 'code' in response_dict["error"]:
                code = response_dict["error"]["code"]
            else:
                # 企业转发接口的格式
                code = response_dict["error"]["type"]

            message = response_dict["error"]["message"]

            if code == "invalid_api_key":
                return f"对不起, 您输入的 key 在OpenAI 官网查询无效，请检查您的 key 是否正确\n " \
                       f"\nOpenAI 官方返回错误信息如下:\n" + message + \
                       f"\n\n如遇使用问题，请回复「功能说明」查看此公众号GPT 相关功能使用技巧，感谢您的理解与支持~"

            if code == "one_api_error":
                if message == "该令牌状态不可用":
                    return "😭对比起，您的账户余额已不足，请联系 LHYYH0001 充值！\n\n" \
                           "✅ 套餐详情：https://ydyrb84oyc.feishu.cn/docx/XO3AdeWXZo5l8YxrGEHcLFo6n5p \n\n" \
                           "✅ 永久免费ChatGPT网站：https://javastarboy.com/ \n" \
                           "🔑 密码：🔥AI2.0实验室交流群更新"
                else:
                    return f"❌ 由于OpenAI官网限制，暂不支持查询官方key余额。\n\n" \
                           f"✅ 目前仅支持查询我为大家提供的 GPT-4 转发 key 余额使用情况！\n\n" \
                           f"[庆祝] GPT4.0 转发API套餐介绍(招代理)\n\n" \
                           f"▶ GPT-4 价格低至 1.3元/1刀 \n" \
                           f"▶ 关注加AGI舰长好友「LHYYH0001」即可免费体验 3-6 次\n" \
                           f"▶ 加入星球可提供更多使用权限\n" \
                           f"▶ 套餐详情：https://ydyrb84oyc.feishu.cn/docx/XO3AdeWXZo5l8YxrGEHcLFo6n5p \n\n" \
                           f"✅ 永久免费ChatGPT网站：https://javastarboy.com/ \n" \
                           f"🔑 密码：🔥AI2.0实验室交流群更新"
            else:
                return subscription_response.text
        except Exception as e:
            print("解析 usage 信息异常" + e)
            return subscription_response.text

    # start_date设置为今天日期前99天
    start_date = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
    # end_date设置为今天日期+1
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    billing_url = f"{baseTxProxyUrl}/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    billing_response = requests.get(billing_url, headers=headers)
    if billing_response.status_code == 200:
        data = billing_response.json()
        total_usage = data.get("total_usage") / 100
    else:
        return billing_response.text

    return f"总额:\t{total:.4f}$\n" \
           f"已用:\t{total_usage:.4f}$\n" \
           f"剩余:\t{total - total_usage:.4f}$\n\n" \
           f"GPT4 可请求次数剩余约: {(total - total_usage) * 25:.0f} 次\n" \
           f"GPT3.5 可请求次数剩余约: {(total - total_usage) * 2000:.0f} 次\n\n" \
           f"有效期至：" + str(access_until) + "\n\n" \
           f"▶ GPT4.0 转发API套餐介绍（低至 1.3 元每刀）🔗 https://ydyrb84oyc.feishu.cn/docx/XO3AdeWXZo5l8YxrGEHcLFo6n5p"

# print(getUsage(settings.Config.chat_gpt_key))
