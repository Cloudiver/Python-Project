import requests
import time
from requests.adapters import HTTPAdapter

session = requests.session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

body = {
    'log': '用户名',
    'pwd': '密码',
    'wp-submit': '登录'
}

url = 'http://www.doki8.com/wp-login.php'
try:
    resp = session.post(url, headers=header, data=body)
    if resp.status_code == 200:
        with open('e:\\log.txt', 'a') as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + '登录成功' + '\n')
except requests.exceptions.RequestException as e:
    with open('e:\\log.txt', 'a') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + str(e) + '\n')


# 查看登录是否成功
# response = session.get('http://www.doki8.com/198652.html', headers=header).text
# print(response)