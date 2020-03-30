import requests
import datetime
import time
import os

"""
下载时候, 容易出错, 原因未知
以后再分析
"""

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': '你的 cookie',
}

# 设置代理
proxy = '127.0.0.1:1080'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

session = requests.session()

# 需要下载画师的详情页
url = 'https://www.pixiv.net/ajax/user/3569577/profile/all'

resp = session.get(url, headers=headers).json()
illusts = resp['body']['illusts']
# 字典只获取键名
illusts_id = [key for key, value in illusts.items()]   # https://blog.csdn.net/qq_33867131/article/details/81019233


# 创建文件夹
def mkdir(path):
    if os.path.exists(path):
        print('文件夹已存在')
    else:
        os.makedirs(path)
        print(path, '创建完成')


"""UTC时间转本地时间（+8: 00）"""
def utc2local(utc_st):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = utc_st + offset
    return local_st


def get_image(id):
    url = 'https://www.pixiv.net/ajax/illust/{0}'.format(id)
    resp = session.get(url, headers=headers, timeout=10).json()
    uploadDate = resp['body']['uploadDate']
    pageCount = resp['body']['pageCount']
    title = resp['body']['title']
    date = datetime.datetime.fromisoformat(uploadDate)
    result = utc2local(date)
    filetype = resp['body']['urls']['original'][-4:]
    # 图片源地址这里应该有问题, 特别是图片后缀
    imgurl_pri = 'https://i.pximg.net/img-original/img/{0}/{1}/{2}/{3}/{4}/{5}/{7}_p{6}' + filetype
    imgurls = []
    with open('e:\\ceshi.txt', 'a') as f:
        for i in range(pageCount):
            img_url = imgurl_pri.format(str(result.year), str(result.month).zfill(2), str(result.day).zfill(2), str(result.hour+1).zfill(2), str(result.minute).zfill(2), str(result.second).zfill(2), str(i), id)
            # resp = session.get(img_url, headers=headers,  timeout=10).content
            imgurls.append(img_url)
            f.write(img_url)

    save_img(imgurls, title, id)


# 保存图片
def save_img(imgurl, title, id):
    path = f'D:\\iPhone\\{title}'
    mkdir(path)  # 保存文件夹设置

    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'Host': 'i.pximg.net',
        'referer': 'https://www.pixiv.net/artworks/' + id,
    }
    for number, ele_image_url in enumerate(imgurl):
        try:
            response = session.get(ele_image_url, headers=header)
            print(ele_image_url)
            if response.status_code == 200:
                with open(path + f'\\{number}{ele_image_url[-4:]}', 'ab') as f:
                    f.write(response.content)
                    print(number, '.jpg 保存成功')
            else:
                print('未获取到图片')
                continue
        except requests.exceptions.RequestException as e:
            print('失败原因:', e)


for ele in illusts_id:
    get_image(ele)