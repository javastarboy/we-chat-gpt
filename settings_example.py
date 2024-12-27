class Config(object):
    """
    若需实现 vercel 读取环境变量方式配置，需要通过如下方式改造代码
    import os
    database_url = os.environ.get('DATABASE_URL')
    """
    # 微信公众号的 token\APP_ID\APP_SECRET
    weToken = 'xxxxxxx'
    APP_ID = "xxxxxxx"
    APP_SECRET = "xxxxxxxxx"

    # api_key，支持英文逗号分割轮训机制 
    chat_gpt_key = 'sk-OQ8b7tdxxxxxxxxxx'
    # 开通 GPT-4 模型的账号，key为FromUserName，value 为对应的个人专属 api_key）
    GPT4_Account = [
        ("xxxxxxxxxxxxxxxx", "sk-OQ8b7tdVKGxxxxxxxxxxxxx"),
        ("FromUserName", "api_key")
    ]
    # 代理服务根地址
    baseTxProxyUrl = "xxxxxxxx"
    # 代理服务 uri 地址/v1/chat/completions
    txProxyUrl = "xxxxxxxx/v1/chat/completions"
    # 企业转发 url
    baseTxProxyTranspondUrl = "xxxxxxxxx"
    # 官网直通 url
    openaiUrl = "https://api.openai.com"

    # session 自动失效时间，秒
    clearSessionTime = 3600
    # 历史对话返回字符长度
    interceptionLength = 1800

    # 语音识别开关
    VoiceSwitch = True
    # 百度语音识别：https://console.bce.baidu.com/ai/?_=1682589061589#/ai/speech/app/list
    BaiDU_APP_ID = 'xxxxxxxxxxx'
    BaiDU_API_KEY = 'xxxxxxxxxxx'
    BaiDU_SECRET_KEY = 'xxxxxxxxxxxx'

    # redis
    host = 'xx.xx.xx.xx'
    port = 6379
    password = 'xxxx'
    db = 0
    # cluster、sentinel、single
    model = "cluster"
    startup_nodes = [
        {'host': 'xx.xx.xx.xx', 'port': 26379},
        {'host': 'xx.xx.xx.xx', 'port': 26380},
        {'host': 'xx.xx.xx.xx', 'port': 26381},
        {'host': 'xx.xx.xx.xx', 'port': 26382},
        {'host': 'xx.xx.xx.xx', 'port': 26383},
        {'host': 'xx.xx.xx.xx', 'port': 26384}]
    sentinel_list = [
        ('xx.xx.xx.xx', '26379'),
        ('xx.xx.xx.xx', '26380'),
        ('xx.xx.xx.xx', '26381'),
        ('xx.xx.xx.xx', '26382'),
        ('xx.xx.xx.xx', '26383'),
        ('xx.xx.xx.xx', '26384')]
