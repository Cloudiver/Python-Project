## 利用Python给微信公众号发送消息

使用的是微信测试公众号

### 1 微信测试公众号配置

```
https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index
```

![snipaste_20200307_192155.png](http://ww1.sinaimg.cn/large/9dc802a0gy1gcll2iwp4jj20xa098jw0.jpg)

1. 测试号信息

![snipaste_20200307_192402.png](http://ww1.sinaimg.cn/large/9dc802a0gy1gcll4lmibpj20ef040q2s.jpg)

2. 关注测试号, 获得微信号

   ![weiixn.jpg](http://ww1.sinaimg.cn/large/9dc802a0gy1gcll9fkfuhj20vp08pwft.jpg)

3. 可用接口信息

   ![weixin_爱奇艺.jpg](http://ww1.sinaimg.cn/large/9dc802a0gy1gclld1c8e9j20vg0dsju3.jpg)

### 2 调用接口

根据需要调用接口, 文档里有相应的说明.

如:

- 客服接口-发消息
- 模板消息(业务通知)(需企业主体)

![snipaste_20200307_193553.png](http://ww1.sinaimg.cn/large/9dc802a0gy1gcllgta5bej20rj04oglm.jpg)

1. 案例

- 第一步: 获取 **access_token**

```
文档地址:
https://developers.weixin.qq.com/doc/offiaccount/Basic_Information/Get_access_token.html

接口地址:
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET

请求方式:
GET
```

```python
import requests

session = requests.session()
# 获取 access_token
def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    # 填入参数
    params = {
        'grant_type': 'client_credential',
        'appid': '你的APPID',
        'secret': '你的secret'
    }
    result = session.get(url, params=params).json()  # 返回字典
    if result.get('access_token'):
        access_token = result['access_token']
    else:
        access_token = None
    return access_token
```

- 第二步: 发送消息

```
文档地址:
https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#7

接口地址:
https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN

请求方式: POST
```

2. 效果

   ![weixinapi.png](http://ww1.sinaimg.cn/large/9dc802a0gy1gclpy20alqj20hj09e75h.jpg)

> 注意: 超过3天(大概)没回复, 就会发送错误. 此时重新再回复一条消息即可.

2. 全部代码

```python
import requests
import json
import time


"""
功能: 微信订阅号 客服接口-发消息
文档地址: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html#7
"""
session = requests.session()


# 获取 access_token
def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    # 填入参数
    params = {
        'grant_type': 'client_credential',
        'appid': '你的APPID',
        'secret': '你的secret'
    }
    result = session.get(url, params=params).json()  # 返回字典
    if result.get('access_token'):
        access_token = result['access_token']
    else:
        access_token = None
    return access_token


# 发送文字消息
def send_text_message(content, openid):
    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
    params = {
        'access_token': get_access_token()
    }
    body = {
        'touser': openid,
        'msgtype': 'text',
        'text': {
            'content': content
        }
    }
    # dict to json
    jsondata = json.dumps(body)  # 需将 dict 转为 json, 不然返回 40003 错误
    result = session.post(url, data=jsondata, params=params).json()
    with open('e:\\text.txt', 'a', encoding='utf-8') as f:
        if result.get('errcode') == 0:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + '发送成功\n')
        else:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + '接口请求错误\n')


if __name__ == '__main__':
    send_text_message('ok', '你的openid,关注测试号后生成')

```

### 3 资料

- [Python 微信公众号发送消息](https://www.cnblogs.com/supery007/p/8136295.html)
- [微信开发errcode:45015,errmsg:response out of time limit之完美解决](https://www.caogenjava.com/detail/79.html)
- [微信小程序API 发送客服消息](https://www.w3cschool.cn/weixinapp/weixinapp-api-custommsg-conversation.html)