import requests

"""
注意: 网址可能发生改变
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    'Host': 'www.tsdm.live',
    "content-type": "application/x-www-form-urlencoded",
    'cookie': "你的 cookies"
}
data = {
    'formhash': 'b4d2d763',
    'qdxq': 'wl',
    'qdmode': '1',
    'todaysay': '无聊',
    'fastreply': '1'
}
url = 'https://www.tsdm.live/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1'

for index in range(5):
    resp = requests.post(url, data=data, headers=headers)
    if resp.status_code == 200:
        print('今天签到成功\n')
        print(resp.text)
        break
    else:
        if index == 4:
            print('签到失败')