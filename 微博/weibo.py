import requests
from datetime import datetime, timedelta
import astral
import time
import http.cookiejar as cookielib
import sys
from serverq import serverq

session = requests.session()

User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
header = {
    'User-Agent': User_Agent
}
"""
astral 1.10.1 版本
"""

# 小号
# 发微博
def send_msg(content):
    session.cookies = cookielib.LWPCookieJar(filename='/root/weibo/weibo.txt')
    session.cookies.load()  # 载入cookies
    if not islogin():  # 没有登录
        login('用户名', '密码')
    st = get_st()  # 获取st

    headers = {
        'Host': 'm.weibo.cn',
        'User-Agent': User_Agent,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'MWeibo-Pwa': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-XSRF-TOKEN': st,
        'Origin': 'https://m.weibo.cn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://m.weibo.cn/compose/',
        'TE': 'Trailers',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    body = {
        'content': content,
        'st': st,  # 10 分钟的有效期
        '_spr': 'screen:1600x900'
    }
    url = 'https://m.weibo.cn/api/statuses/update'
    resp = session.post(url, data=body, headers=headers)
    if resp.status_code == 200:
        try:
            data = resp.json()
            status = data['ok']
            if status == 1:
                print(time.strftime('%Y-%m-%d %H:%M:%S '), '发送成功')
            else:
                serverq('微博发送失败')
        except:
            serverq('微博发送失败')
    else:
        serverq('微博发送失败')


# 登录
def login(username, password):
    headers = {
        'Host': 'passport.weibo.cn',
        'User-Agent': User_Agent,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://passport.weibo.cn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://passport.weibo.cn/signin/login'
    }

    postdata = {
        'username': username,
        'password': password,
        'savestate': '1',
        'r': "https://m.weibo.cn/",
        'ec': '0',
        'entry': 'mweibo',
        'wentry': '',
        'loginfrom': '',
        'client_id': '',
        'code': '',
        'qq': '',
        'mainpageflag': '1',
        'hff': '',
        'hfp': ''
    }
    url = 'https://passport.weibo.cn/sso/login'
    resp = session.post(url, headers=headers, data=postdata)
    session.cookies.save()  # 保存 cookies


# 获取 st
def get_st():
    url = 'https://m.weibo.cn/api/config'
    resp = session.get(url, headers=header)
    st1 = resp.json()['data']['st']
    return st1


# 判断当前是否登录
def islogin():
    url = 'https://m.weibo.cn/api/config'
    resp = session.get(url, headers=header)
    login_state = resp.json()['data']['login']
    # print(resp.json())
    if resp.status_code == 200:
        if login_state:
            return True
        else:
            print('未登录')
            return False
    else:
        return False


# 经纬度坐标
# 114.420023,30.514722
def sunshine():
    location_nandamen = astral.Location(('Hust', 'China', 30.514722, 114.420023, 'Asia/Shanghai', 0))
    today = datetime.now()
    sunrise = location_nandamen.sunrise(date=today.date(), local=True)  # datetime
    sunset = location_nandamen.sunset(date=today.date(), local=True)
    tomorrow = today + timedelta(days=1)
    sunrise_tomorrow = location_nandamen.sunrise(date=tomorrow.date(), local=True)
    sun = [sunrise, sunset, sunrise_tomorrow]
    return sun


# 时间精确到分
def getdatetime(dates):
    hour = dates.hour
    minute = dates.minute
    if dates.second > 30:
        minute += 1
        if minute == 60:
            hour += 1
            minute = 0
    return str(hour).zfill(2) + ':' + str(minute).zfill(2)


# 倒计时功能
def countdown(t, step=1, msg='sleeping'):  # in seconds
    pad_str = ' ' * len('%d' % step)
    for i in range(t, 0, -step):
        print('%s for the next %d seconds %s' % (msg, i, pad_str))
        # sys.stdout.flush()
        time.sleep(step)
    print('Done %s for %d seconds! %s' % (msg, t, pad_str))


# 主程序
def main():
    now_time = datetime.now()
    sun = sunshine()
    if now_time.timestamp() <= sun[0].timestamp():
        countdown(int(sun[0].timestamp() - now_time.timestamp()))
        sunset = getdatetime(sun[1])
        content = '#武汉日出# 太阳升起来了, 今天的日落时间是' + sunset
        send_msg(content)
    elif sun[1].timestamp() >= now_time.timestamp() > sun[0].timestamp():
        countdown(int(sun[1].timestamp() - now_time.timestamp()))
        sunrise_tomo = getdatetime(sun[2])
        content = '#武汉日落# 太阳下山了, 明天的日出时间是' + sunrise_tomo
        send_msg(content)
    else:
        return 'next day'


if __name__ == '__main__':
    main()
