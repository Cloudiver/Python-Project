import falcon
import re
import requests
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply


"""
公众号开发
参考: 
关注/取消关注事件: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html
被动回复消息: https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html#0
代码: https://segmentfault.com/a/1190000015271082

waitress-serve --port=80 autosend:app 启动
"""
class Connect(object):

    def on_get(self, req, resp):
        query_string = req.query_string
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]

        try:
            check_signature(token='your_token', signature=b['signature'], timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    # 一言
    def hitokoto(self):
        resp = requests.get('https://v1.hitokoto.cn/?c=a')
        if resp.status_code == 200:
            try:
                data = resp.json()
                content = data.get('hitokoto') + '\n' + 'from: 「' + data.get('from') + '」'
                return content
            except:
                return '喵帕斯不知道呢~'
        else:
            return '喵帕斯不知道呢~'

    # 番剧更新
    def bangumi(self):
        url = "https://bangumi.bilibili.com/web_api/timeline_global"
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            try:
                data = resp.json()
                result = data['result']   # list
                content = ''
                for ele in result:
                    if ele.get('is_today'):
                        seasons = ele.get('seasons')
                        if len(seasons) != 0:
                            for season in seasons:
                                if season.get('delay') == 0:   # 没有延期
                                    bangbumi_title = season['title']
                                    favorites = str(season['favorites'])  # 追番人数
                                    pub_index = season.get('pub_index')   # 更新集数
                                    pub_time = season['pub_time']   # 更新时间
                                    is_published = season.get('is_published')   # 查询时是否已经更新
                                    published = ''
                                    if is_published == 1:
                                        published = '(已更新)'
                                    content += '番剧: ' + bangbumi_title + '\n' \
                                               '追番人数: ' + favorites + '\n' \
                                               '更新: ' + pub_index + published + '\n' \
                                               '更新时间: ' + pub_time + '\n\n'
                            return '今日更新\n' + content.strip()
                        else:
                            return '今天没有番剧更新'
            except:
                return '喵帕斯不知道呢~'
        else:
            return '喵帕斯不知道呢~'

    # 获取bilibili直播间源地址
    def get_url(self, roomid):
        pattern = re.search(r'\d{1,8}', roomid)
        roomid = pattern.group(0)
        url = 'http://api.live.bilibili.com/room/v1/RoomStatic/get_room_static_info?room_id=' + roomid
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
        }
        resp = requests.get(url, headers=header)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data['code'] == 0:
                    up = data['data']['uname']
                    title = '标题: ' + data['data']['title']
                    if data['data']['live_status'] == 1:
                        online = '人气: ' + str(data['data']['online'])
                        msg = 'up: ' + up + '\n' + title + '\n' + online
                        # resp = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid=' + roomid + '&qn=10000&platform=web', headers=header)
                        # if resp.status_code == 200:
                        #     data = resp.json()
                        #     if data['code'] == 0 and data['data'] is not None:
                        #         durl = data['data']['durl'][0]['url']
                        return msg
                    else:
                        return up + '没有开播'
                else:
                    return '喵帕斯休息了'
            except:
                return '喵帕斯不知道呢~'
        else:
            return '喵帕斯抽风了, 稍后再来'

    def on_post(self, req, resp):
        xml = req.stream.read()
        msg = parse_message(xml)
        if msg.type == 'text':
            content = msg.content
            if content.isdigit():
                text = Connect().get_url(content)
                reply = TextReply(content=text, message=msg)
            elif content == '一言':
                text = Connect().hitokoto()
                reply = TextReply(content=text, message=msg)
            elif content == 'anime':
                text = Connect().bangumi()
                reply = TextReply(content=text, message=msg)
            elif content == '迅雷':
                text = 'Safari打开:\nhttps://ithunder-ota.a.88cdn.com/download-guide/step1.html?from=gzhlm'
                reply = TextReply(content=text, message=msg)
            elif content == '哔咔':
                text = '浏览器打开:\nhttps://download2.picacomiccn.xyz'
                reply = TextReply(content=text, message=msg)
            else:
                reply = TextReply(content=content, message=msg)
        elif msg.type == 'event' and msg.event == 'subscribe':
            help = "谢谢关注!\n\n" \
                   "1. 在对话框输入'哔咔', 获取哔咔下载地址\n\n" \
                   "2. 输入'迅雷', 获取iOS版迅雷下载地址\n\n" \
                   "3. 输入'一言', 可以看到一句台词\n\n" \
                   "4. 输入'anime', 查看今天更新的番剧\n\n" \
                   "5. 输入b站直播房间号, 如'1017', 可以查看当前主播是否在线"
            reply = TextReply(content=help, message=msg)
        else:
            reply = TextReply(content="只支持文字消息", message=msg)
        xml = reply.render()
        resp.body = (xml)
        resp.status = falcon.HTTP_200


app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)
