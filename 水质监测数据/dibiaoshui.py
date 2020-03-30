import requests
import csv
import time
import json
from datetime import datetime

"""
环保部地表水监测数据, 每隔1h获取1次
"""

session = requests.session()

headers = {
    'Host': '123.127.175.45:8082',
    'Proxy-Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://123.127.175.45:8082',
    'Referer': 'http://123.127.175.45:8082/'
}

url = 'http://123.127.175.45:8082/ajax/GwtWaterHandler.ashx'
postdata = {
    'Method': 'SelectRealData'
}


# 获取数据
def get_data():
    for i in range(5):
        try:
            resp = session.post(url, headers=headers, data=postdata, timeout=10)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.json()
        except:
            print('出现错误, 等待1秒')
            time.sleep(1)
    return 'False'


def write_data(data):
    if len(data) != 0:
        today = str(datetime.now().date())
        with open(f'e:\\{today}.csv', 'a', newline='') as f:
            fieldnames = ['断面名称', '测量时间', 'ph', '溶解氧', '氨氮', '高锰酸盐指数', '总有机碳', '水质类别', '断面属性', '站点情况']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ele in data:
                writer.writerow({
                    '断面名称': ele['siteName'], '测量时间': ele['dateTime'], 'ph': ele['pH'], '溶解氧': ele['DO'],
                    '氨氮': ele['NH4'], '高锰酸盐指数': ele['CODMn'], '总有机碳': ele['TOC'], '水质类别': ele['level'],
                    '断面属性': ele['attribute'], '站点情况': ele['status']
                })
        with open('/home/g/dibiaoshui.txt', 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S ' + f'写入{len(data)}条数据\n'))


# 发送错误信息
def sendmsg(msg):
    header = {'content-type': 'application/json'}

    url = 'http://wxpusher.zjiecode.com/api/send/message'

    postdata = {
        'appToken': 'wxpusher token',
        'content': msg,
        'contentType': 1,
        'uids': ['wxpusher uids'],
        'url': ''
    }

    resp = session.post(url, headers=header, data=json.dumps(postdata)).json()
    with open('/home/g/dibiaoshui_error.txt', 'a') as f:
        if resp['data'][0]['code'] == 1000:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送成功\n')
        else:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S') + '发送失败\n')


while True:
    data_list = get_data()  # 获取数据
    if data_list == 'False':
        sendmsg('[地表水数据]请求错误, 请查看接口是否更换')
        break
    write_data(data_list)   # 写入数据
    time.sleep(3600)
