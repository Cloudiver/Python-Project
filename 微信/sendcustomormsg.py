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
