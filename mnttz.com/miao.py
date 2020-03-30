import requests
from requests.adapters import HTTPAdapter
from lxml import etree
import os
import time

"""
爬取mnttz.com
"""
session = requests.session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))

# 代理设置
proxy = '127.0.0.1:1080'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}


# 获取地址ID和标题
def get_data():
    url = 'https://www.mnttz.com/gctt/page/{0}'
    # 第一次请求
    resp = session.get(url.format(1), headers=header, timeout=10, proxies=proxies).content
    html = etree.HTML(resp)

    pid_xpath = '//article/footer/a/@data-pid'
    title_xpath = '//article/h2/a/text()'
    total_page_xpath = '//ul/li/span/text()'
    pid = html.xpath(pid_xpath)  # pid--可以拼接得到链接
    title = html.xpath(title_xpath)  # 套图标题
    total_page = int(html.xpath(total_page_xpath)[-1].replace(' ', '')[-3:-1])  # 总页码
    # 第一次请求完毕

    # 开始遍历所有页码
    for index in range(2, total_page + 1):   # 从第二页到尾页
        resp = session.get(url.format(index), headers=header, timeout=10, proxies=proxies).content
        html = etree.HTML(resp)
        pid.extend(html.xpath(pid_xpath))
        title.extend(html.xpath(title_xpath))

    data = {'pid': pid, 'title': title}
    return data


# 获取每页的图片地址
def getimg_url(data):
    pid = data.get('pid')  # 返回pid 形式为列表
    title = data.get('title')   # 返回标题
    url = 'https://www.mnttz.com/{191098}/page-{1}.html'
    for pid_index, data_pid in enumerate(pid):
        # 获取第一页信息  每个地址只需要第一页信息,就可以获取所有的图片地址
        resp = session.get(url.format(data_pid, 1), headers=header, timeout=10, proxies=proxies).content
        html = etree.HTML(resp)
        imgurl_xpath = '//div[@class="content"]/article[@class="article-content"]/p/img/@src'
        imgurl = html.xpath(imgurl_xpath)   # 第一页的图片url

        # 根据第一页, 获取总共有多少页
        page_xpath = '//div[@class="article-paging"]/a/span/text()'
        page_num = int(html.xpath(page_xpath)[-1])   # 每个地址有多少页图片

        if page_num >= 2:   # 如果页码大于1
            for index in range(2, page_num + 1):   # 循环获取该pid的所有图片地址
                resp = session.get(url.format(data_pid, index)).content
                html = etree.HTML(resp)
                imgurl.extend(html.xpath(imgurl_xpath))

        # 遍历获取到的图片地址, 开始保存
        save_img(imgurl, title[pid_index])  # 保存图片
        print(title[pid_index], '保存成功')


# 保存图片
def save_img(imgurl, title):
    path = f'D:\\share\\图集\\photos\\pian\\{title}'
    mkdir(path)  # 保存文件夹设置
    for number, ele_image_url in enumerate(imgurl):
        try:
            response = session.get('https:' + ele_image_url, headers=header, timeout=10, proxies=proxies)
            if response.status_code == 200:
                with open(path + f'\\{number}.jpg', 'ab') as f:
                    f.write(response.content)
                    print(number, '.jpg 保存成功')
            else:
                print('未获取到图片')
                continue
        except requests.exceptions.RequestException as e:
            print('失败原因:', e)


# 创建文件夹
def mkdir(path):
    if os.path.exists(path):
        print('文件夹已存在')
    else:
        os.makedirs(path)
        print(path, '创建完成')


if __name__ == '__main__':
    datas = get_data()
    getimg_url(datas)