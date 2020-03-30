import requests
from wx import sendmsg
import time

"""
b站直播间开播通知(5分钟请求一次)
为什么不用官方的通知?
app打开通知设置会推送其他无关内容, 且该程序可以检测直播间标题的变化,
当同一个直播间直播内容发生改变的时候, 也会提醒.
微信推送借助: wxpusher(http://wxpusher.zjiecode.com/docs/#/)
"""

session = requests.session()
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    "cookie": "SESSDATA=你的data值"
}


def live_notice():
    url = 'http://api.live.bilibili.com/relation/v1/feed/feed_list'
    resp = session.get(url, headers=header)
    if resp.status_code == 200:
        data = resp.json()
        if data['code'] == 0:  # 请求状态成功
            if data['data']['results'] > 0:
                live_rooms = data['data']['list']
                with open('/home/g/bilibili/live.txt', 'r', encoding='utf-8') as f1:
                    msg_list = f1.readlines()   # 读取文本中的所有数据
                # print(msg_list)
                msg_list = [x.strip() for x in msg_list]  # 去除末尾的换行 \n
                # print(msg_list)

                with open('/home/g/bilibili/live.txt', 'w', encoding='utf-8') as f2:
                    notice_msg = ''   # 最后需要通知的信息
                    for live_room in live_rooms:
                        _str = live_room['uname'] + '|' + live_room['title']
                        if msg_list.count(_str) == 0:   # 这个是新开播的内容, 通知
                            notice_msg = notice_msg + _str + '\n'
                        f2.write(live_room['uname'] + '|' + live_room['title'] + '\n')  # 重新写入开播信息
                    # print(notice_msg)
                if notice_msg != '':
                    sendmsg(notice_msg)
            return True
        else:
            sendmsg('bilibili的cookie已失效, 请重新设置')   # cookie有效期 6 个月
            return False


if __name__ == '__main__':
    while True:
        if not live_notice():
            break
        else:
            time.sleep(300)   # 休眠5分钟
