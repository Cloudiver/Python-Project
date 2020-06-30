import requests
from lxml import etree
import re
import execjs
import sys


s = requests.session()

proxy = '127.0.0.1:10808'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

# 接收参数
# url = str((sys.argv)[1])


url = 'https://cn.pornhub.com/view_video.php?viewkey=ph5ee5837fe02aa'

r = s.get(url, headers=headers)
htmlContent = r.content
htmlContent = etree.HTML(htmlContent)

#先爬核心段内容，以便获取videoId
all = htmlContent.xpath('//div[@id="player"]')[0]
all = etree.tostring(all, encoding='utf-8')
# print(all)


videoId = re.findall('data-video-id="(.+?)"', str(all))[-1]
# print(videoId)
#再爬js内容
js = htmlContent.xpath('//div[@id="player"]/script/text()')[0]
#执行js
#需要补充完整
jscontext = execjs.compile("var loadScriptVar=[];var loadScriptUniqueId=[];var playerObjList = {};"+js)
#获取flashvars_变量
res = jscontext.eval('flashvars_' + videoId)   # 注意中文乱码问题

"""
代码: https://bugxia.com/1409.html
乱码解决: https://blog.csdn.net/suwenlai/article/details/93047182  lib/subprocess.py(成功解决)
另外方法: https://segmentfault.com/q/1010000016025598   (未尝试)
"""

# 标题
print(res['video_title'])
# 视频地址
# print(res['mediaDefinitions'])  # list
mediaDefinitions = res['mediaDefinitions']  # 视频参数信息
print('清晰度: ' + mediaDefinitions[0]['quality'] + '\n' + '视频地址: ' + mediaDefinitions[0]['videoUrl'])
