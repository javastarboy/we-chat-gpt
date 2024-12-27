import requests
from aip import AipSpeech
import settings

# 百度语音识别 API 配置
APP_ID = settings.Config.BaiDU_APP_ID
API_KEY = settings.Config.BaiDU_API_KEY
SECRET_KEY = settings.Config.BaiDU_SECRET_KEY

# 初始化百度语音识别客户端
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取语音文件
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


def getContent(filepath):
    # 语音识别 1537-普通话(纯中文识别) 【https://ai.baidu.com/ai-doc/SPEECH/0lbxfnc9b】

    try:
        result = client.asr(get_file_content(filepath), 'amr', 16000, {'dev_pid': 1537})
        if result['err_no'] == 0:
            return result['result'][0]
        else:
            raise ValueError("转语音失败" + str(result))
    except Exception as e:
        print(e)
        raise e
