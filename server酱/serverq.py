import requests


# server酱消息通知
def serverq(content):
    header = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    datas = {
        'text': 'SunriseBot服务消息',   # 标题
        'desp': content    # 详细内容
    }
    url = 'https://sc.ftqq.com/[TOKEN].send'
    resp = requests.post(url, data=datas, headers=header)


if __name__ == '__main__':
    serverq('')
