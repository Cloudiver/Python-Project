import requests
import json
import time

"""
微信通知
"""
def sendmsg(msg):
    session = requests.session()
    headers = {'content-type': 'application/json'}

    url = 'http://wxpusher.zjiecode.com/api/send/message'

    postdata = {
        'appToken': '你的token',
        'content': msg,
        'contentType': 1,
        # 'topicIds': [132],
        'uids': ['微信关注后的 uid'],
        'url': ''
    }

    resp = session.post(url, headers=headers, data=json.dumps(postdata)).json()
    with open('/home/g/bilibili/bilibili_live.txt', 'a') as f:
        if resp['data'][0]['code'] == 1000:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送成功\n')
        else:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送失败\n')


if __name__ == '__main__':
    sendmsg('')
