import requests
from aip import AipSpeech

# 百度语音识别 API 配置
import settings
from pydub import AudioSegment
import io
import requests

APP_ID = settings.Config.BaiDU_APP_ID
API_KEY = settings.Config.BaiDU_API_KEY
SECRET_KEY = settings.Config.BaiDU_SECRET_KEY

# OpenAI GPT-3 API 配置
OPENAI_API_KEY = settings.Config.chat_gpt_key
OPENAI_API_URL = settings.Config.txProxyUrl

# 初始化百度语音识别客户端
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 从微信公众号获取语音文件并保存到本地
voice_url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token=c345h654a78p234t567&media_id=uXgBZPpt0kjSEwI8ZELRfpuYmJKb8tA3_QTYcxsQFQtZJu05T__Pf8aKERvMZA-5'

# filepath = "voice/16k-23850.amr"
# response = requests.get(voice_url)
# with open(filepath, 'wb') as f:
#     f.write(response.content)
#

# 从微信公众号语音消息的 URL 中获取音频数据
response = requests.get(voice_url)
audio_data = io.BytesIO(response.content)

# 将音频数据转换为 AudioSegment 对象
audio_segment = AudioSegment.from_file(audio_data)
filepath = "voice/audio.wav"

# 将音频数据转换为 wav 格式
audio_segment.export(filepath, format="wav")

# 读取语音文件
def get_file_content(filepath):
    with open(filepath, 'rb') as fp:
        return fp.read()


# 语音识别
result = client.asr(get_file_content(filepath), 'wav', 16000, {'dev_pid': 1537})

print(result)

