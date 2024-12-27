# WeChatGPT_JSB

## 介绍
本项目实现了【微信公众号对接OpenAI】，实现了 ChatGPT 聊天对话功能，仅需要手机与公众号聊天即可，其余的交给代码实现。 没有任何门槛。
- 先给大家看下效果（大家也可以先关注公众号体验一下）
- 支持文本、语音消息向 GPT 提问
- 公众号二维码
<div style="text-align:center">
    <img src="pictures/公众号二维码.png">
</div>

## 软件架构
- Python 3.9+
- Flask 架构
- Redis 集群
- OpenAI、微信公众平台普通消息接口
- 开启微信语音识别功能，也可不开启，就只纯文本也行

## 安装教程
1.  使用 pip 进行安装模块
    ```
    # 进入项目目录上传源码（路径自己定）
    cd /home/tomcat/wechatgpt/logs
    # 上传代码
    
    # 安装虚拟环境
    python3 -m venv venv
    
    # 激活并安装依赖
    source venv/bin/activate
    
    # 如果镜像安装有问题，可以 pip config list 查看镜像源（能看到 pip.conf）
    
    # 如果报错较多，就升级一下 pip 版本，pip3 install --upgrade pip
    
    pip3 install -r requirements.txt
    
    # 创建日志文件目录并授权
    cd /path/to/your/project
    mkdir -p /home/tomcat/wechatgpt/logs
    chmod 755 /home/tomcat/wechatgpt/logs
    ```
2. 运行 
    ```commandline
    python3 WeChatController.py
    # 或后台启动
    nohup python3 WeChatController.py >/dev/null 2>&1 &
    # 后台启动并输出日志
    nohup python3 WeChatController.py > /home/tomcat/wechatgpt/logs/wechatgpt.log 2>&1 &
    # 查看日志
    tail -f /home/tomcat/wechatgpt/logs/wechatgpt.log
   
    # 验证
    浏览器访问：http://your_domain/chatgpt, 得到响应结果即部署成功
    接下来到微信公众号后台“安全中心以及基本配置”菜单下配置【域名、IP白名单】即可
    注意：别忘了放开服务器端口，防火墙等
   
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
    ```
3. 停服
    ```
    kill $(ps -ef | grep "python3 WeChatController.py" | grep -v grep | awk '{print $2}')
    ```

## 使用说明

#### 【1】settings.py 说明
| key                  | value 含义            | 说明                                             |
|----------------------|---------------------|------------------------------------------------|
| weToken              | 微信公众号的 token        | 需要开通并启用服务器配置（需要域名）                             |
| chat_gpt_key         | openai 的的 api_key   | 不会申请的看我公众号：AGI舰长                         |
| txProxyUrl           | 腾讯云服务器函数服务，跳转硅谷区域代理 | 也可使用其他代理方式                                     |
| clearSessionTime     | 会话 session 自动失效时间，秒 | 超过此时间清空会话记录，也可不清空，看自己意愿                        |
| interceptionLength   | 历史对话返回字节长度          | 微信支持的最大字节 2048，大概 600 个汉字左右                    |
| host、port、password 、db | redis 单机配置方式        | 此项目使用的集群模式，工具类 RedisUtil.py 也是集群，如果用单机，改一下代码即可 |
| startup_nodes   | 集群的配置节点             | 工具类 RedisUtil.py                                         |
| sentinel_list          | 哨兵模式的配置节点       | 工具类 RedisUtil.py                                        |


#### 【2】代理服务说明
我用的是腾讯云的函数代理服务，购买的是美国硅谷服务器，所以网络问题自然不存在了。
随时可用，没有门槛，解决了大问题了。
需要教程的关注我微信公众号：「AGI舰长」即可获取。

#### 【3】微信公众号服务器配置启用说明

`需要详细教程的也可以关注我微信公众号：AGI舰长 即可获取。`
- 登录 [微信公众平台](https://mp.weixin.qq.com/)
- 点击左侧菜单【设置与开发】
- 点击菜单【基本配置】
- 下滑配置【服务器配置】
- 填写【服务器地址(URL)】与【令牌(Token)】
- 右侧点击【启用】
  > 注意：如果不启用是没效果的，同时自定义的菜单、自定义回复都将失效

## 功能清单

- [x] 回复消息「功能说明」查看功能清单与使用说明并获取见面礼福利
- [x] 支持文本、语音向 GPT3.5、GPT-4 双模型提问
- [x] 回复消息「查询余额+你的api_key」可以查看你的账户余额情况
- [x] 回复消息「继续」查看 ChatGPT 最近一次回答内容
- [x] 回复消息「历史对话」记录查看
- [x] 回复消息「继续写」让 ChatGPT 输出新的回答
- [x] 回复消息「stop」清空会话记录
- [ ] 客服消息接口对接，延迟消息自动回复给用户，彻底解决手动回复 「继续」获取结果

## 业务对接流程图

![](pictures/微信公众号对接ChatGPT流程图.jpeg)

## ChatGPT 网页版以及学习手册等福利
- AI工具集导航 · AI网址大全
    - https://tools.lhagi.com/

- 大模型API_Key企业中转 && 三款免费的AI聚合工具
    - https://javastarboy.com/

- AI 大模型全栈通识课介绍
    - https://www.yuque.com/lhyyh/agi/introduce

- AGI舰长个人简介
    - https://www.yuque.com/lhyyh/ai/readme

# AI大模型全栈通识课

如果你觉得我的分享对比有帮助，也欢迎加入我们交流社群，每天都有很多关于 ChatGPT、人工智能 AI、Python、变现创业的相关分享。
[点我查看课程介绍](https://www.yuque.com/lhyyh/agi/introduce)

<div style="text-align:center">
    <img src="pictures/详情页.jpg">
</div>

# ✅ 联系我
## AI全栈微信群
<div style="text-align:center">
   <img src="pictures/微信交流群.png">
</div>

## 个人微信
<div style="text-align:center">
    <img src="pictures/个人企微二维码.png">
</div>

## 抖音号
<div style="text-align:center">
    <img src="pictures/抖音号.jpg"  width="400" height="600">
</div>

# 赞助

***
如果你觉得这个项目对你有帮助，并且情况允许的话，可以给我一点点支持，总之非常感谢支持～

## 微信
<div style="text-align:center">
    <img src="pictures/微信收款码.png">
</div>

## 支付宝
<div style="text-align:center">
    <img src="pictures/支付宝收款码.png">
</div>
