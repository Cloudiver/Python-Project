import requests
from lxml import etree
from Crypto.Cipher import AES
import os
import base64
import time

s = requests.session()

proxy = '127.0.0.1:1080'
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
}

url = 'https://www.manhuadui.com/manhua/haizeiwang/'

try:
    resp = s.get(url, headers=headers, proxies=proxies)
    content = resp.content
    html = etree.HTML(content)
    commic_title = html.xpath("//div[@class='comic_i_img']/img/@alt")[0]
    page_urls = html.xpath("//ul[@id='chapter-list-1']/li/a/@href")
    page_urls.reverse()
    page_titles = html.xpath("//ul[@id='chapter-list-1']/li/a/@title")  # 返回列表
    update_time = html.xpath("/html/body/div[3]/div[1]/div[5]/div[1]/span[2]/text()")[0].lstrip('[ ').rstrip(']')
    page_titles.reverse()
except:
    print('暂时无法访问该网站')


# 每话所有图片链接
def images_urls(text):
    total_images = text[text.find("chapterImages") + 17: text.find("chapterPath") - 6]
    base_text = base64.b64decode(total_images)
    decipher = AES.new(b'123456781234567G', AES.MODE_CBC, b'ABCDEF1G34123412')
    result = decipher.decrypt(base_text)
    str_result = result.decode(encoding='utf-8')  # 不知道这个乱码怎么产生的(应该是解码的时候补充出来的)
    str_result = str_result[:str_result.rfind('.jpg') + 4]
    str_to_list = str_result.lstrip('[').replace("\"", "").split(',')

    chapterPath = text[text.find("chapterPath") + 15:text.find("chapterPrice") - 6]
    # 完整路径
    for index, elment in enumerate(str_to_list):
        img_url = 'https://img01.eshanyao.com/' + chapterPath + elment
        str_to_list[index] = img_url
    return str_to_list


def details(flag):
    if not flag:
        for i, ele in enumerate(page_urls):
            r = s.get(url='https://www.manhuadui.com' + ele, headers=headers, proxies=proxies)
            text = r.text
            str_to_list = images_urls(text)
            save(str_to_list, page_titles[i])
    else:
        r = s.get(url='https://www.manhuadui.com' + page_urls[0], headers=headers, proxies=proxies)
        text = r.text
        str_to_list = images_urls(text)
        save(str_to_list, page_titles[0])


# 创建文件夹
def dirmk(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print(path, '创建完成')
    else:
        print('文件夹已经存在')


# 下载图片
def save(img_url, page_titles):
    path = 'c:/' + commic_title + '/' + page_titles
    dirmk(path)
    for index, ele in enumerate(img_url):
        if not os.path.exists(path + f'/{index+1}.jpg'):
            resp = s.get(ele, headers=headers, proxies=proxies)
            if resp.status_code == 200:
                content = resp.content
                with open(path + f'/{index+1}.jpg', 'ab') as f:
                    f.write(content)
    print(time.strftime('%Y-%m-%d %H:%M:%S '), page_titles + '下载完成')


def start():
    try:
        info = commic_title + '\n最新一话: ' + page_titles[0] + '\n' + update_time + '\n' + url
        print(info)
        print('------------------------------------------------')
        isdownload = input("是否下载? 下载最新话输入1, 下载全部输入2, 取消下载输入0:  ")
        flag = True
        if isdownload == '2':
            flag = False   # 下载全部
        elif isdownload == '0':
            return '你已取消下载!'
        path = 'c:/' + commic_title
        dirmk(path)
        details(flag)
    except:
        print('请再次尝试!')


if __name__ == '__main__':
    start()
