import requests
import json
import ncov
import time


def sendmsg():
    session = requests.session()
    headers = {'content-type': 'application/json'}

    url = 'http://wxpusher.zjiecode.com/api/send/message'

    postdata = {
        'appToken': 'wxpusher token',
        'content': msg,
        'contentType': 1,
        # 'topicIds': [132],
        'uids': ['wxpusher uids'],
        'url': ''
    }

    resp = session.post(url, headers=headers, data=json.dumps(postdata)).json()
    with open('/home/g/ncov.txt', 'a') as f:
        if resp['data'][0]['code'] == 1000:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送成功\n')
        else:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送失败\n')


if __name__ == '__main__':
    msg = ncov.getncovmsg()
    sendmsg()
