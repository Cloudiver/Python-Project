# encoding=utf-8
import requests
import json
import csv
import time

"""
爬取b站所有番剧列表
"""

url = 'https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page={0}&season_type=1&pagesize={1}&type=1'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Referer": "https://www.bilibili.com/anime/index/",
    "Host": "api.bilibili.com"
}
session = requests.session()
resp = session.get(url.format(1, 9999), headers=header).text
jsondata = json.loads(resp)
if jsondata['code'] == 0:
    pagesize = round(jsondata['data']['total'] / 20)  # 总页数
    with open('e:\\AnimeListTest.csv', 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['title', 'badge', 'cover', 'index_show', 'is_finish', 'link', 'order']
        count = 1  # 计数器
        while count <= pagesize:
            total = json.loads(session.get(url.format(count, 20), headers=header).text)
            lists = total['data']['list']

            for index, ele in enumerate(lists):
                if index == 0 and count == 1:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                # if ele['media_id'] == 21988886:
                #     continue
                if ele['is_finish'] == 1:
                    ele['is_finish'] = '已完结'
                else:
                    ele['is_finish'] = '正在放送'
                writer.writerow({'title': ele['title'], 'badge': ele['badge'], 'cover': ele['cover'], 'index_show': ele['index_show'],
                                 'is_finish': ele['is_finish'], 'link': ele['link'], 'order': ele['order']})
            print(time.strftime('%Y-%m-%d %H:%M:%S') + f' {ele["title"]}写入完成')
            count += 1
    print('===========')
    print(time.strftime('%Y-%m-%d %H:%M:%S'), '全部数据写入完成')
else:
    print('接口请求错误')
