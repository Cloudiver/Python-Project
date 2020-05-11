import requests
import json
import re
import sys


s = requests.session()

proxy = '127.0.0.1:1080'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

# url = str(sys.argv[1])

url = 'https://www.youtube.com/watch?v=JEg5WfZnr8E'

r = s.get(url, headers=headers, proxies=proxies).text
res = r[r.find('ytplayer.config')+18:r.find('ytplayer.web_player_context_config')-1]
data = json.loads(res.encode('utf-8').decode('utf-8').replace(r'\\u0026', '&'))
player_response = json.loads(data['args']['player_response'])   # 视频信息
urls = player_response['streamingData']['adaptiveFormats']
info = player_response['microformat']['playerMicroformatRenderer']
title = info['title']['simpleText']   # 标题
publishDate = info['publishDate']   # 发布日期
viewCount = info['viewCount']   # 观看人数
time = int(info['lengthSeconds'])   # 视频时长(s)
description = info['description']['simpleText']  # 视频描述
if time > 60:
    time = round(time / 60, 2)

print('标题: ' + title + '\n发布日期: ' + publishDate + '\n视频时长: ' + str(time) + '分\n观看人数: ' + viewCount + '\n描述: ' + description)
print('--------------------------------------')


for index, ele in enumerate(urls):
    # 编码测试文章: https://motovlog.com/threads/making-1080p60-look-like-4k-by-getting-youtubes-bigger-bit-rate.17619/post-156037

    # video_av01 = re.findall('video/.+codecs="av01.+"', ele['mimeType'])   # 视频编码  最好
    # video_vp9 = re.findall('video/.+codecs="vp9"', ele['mimeType'])   # 视频编码  次之  没有声音
    video_avc = re.findall('video/.+codecs="avc.+"', ele['mimeType'])   # 视频编码  最差  不能下载1080p以上

    audio = re.findall('audio/.+codecs="mp4a.+"', ele['mimeType'])   # 音频编码  findall 返回 list  opus 好于m4a, 但是很少有播放器支持

    if video_avc:
        print('视频分辨率: ' + ele['qualityLabel'] + '  ' + ele['url'])
    if audio:
        print('音频(m4a): ' + ele['url'])