import requests


# server酱消息通知
def serverq(content):
    header = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    datas = {
        'text': 'SunriseBot服务消息',
        'desp': content
    }
    url = 'https://sc.ftqq.com/[token]'
    resp = requests.post(url, data=datas, headers=header)


if __name__ == '__main__':
    serverq('')
