from flask import Flask, request

import WeChatRobot

app = Flask(__name__)

# token是微信公众号用来指定接入当前云服务器的服务的凭证，代表是自己人接入的，等一下就有什么用了
# robot = werobot.WeRoBot(token=weToken)
outputContent = []
hasRequest = None


@app.route("/chatgpt", methods=['Post', 'GET'])
def chatgpt():
    # 验证 token
    if request.method == 'GET':
        print("微信 token 验证")
        return WeChatRobot.checkToken()
    else:
        return WeChatRobot.chatRobot()


"""
如果你80端口被占用了，也可以用其他端口，如 808，然后配置Nginx代理
公众号后台地址为：https://域名/chatgpt

server{
   server_name 你的域名;
   
   # 微信公众号AI对话
   location /chatgpt/ {
        proxy_http_version 1.1;
        proxy_pass http://localhost:808/chatgpt;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header Accept-Encoding gzip;
        proxy_read_timeout 300s;
    }
}
"""
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=808, threaded=True)
