import requests
import os
import re
import time

session = requests.session()

headers = {
    'Host': 'api.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Connection': 'keep-alive'
}


# python 3.7 以上
def process(url, header, title):
    fileName = re.sub('[\\/:*?"<>|]', '-', title)
    start = time.time()
    size = 0
    for index in range(5):
        response = session.get(url, headers=header, stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
        if response.status_code == 200:
            chunk_size = 1024  # 每次块大小为1024
            content_size = int(response.headers['content-length'])  # 返回的response的headers中获取文件大小信息
            print("文件大小：" + str(round(float(content_size / chunk_size / 1024), 1)) + " MB")
            with open(f'c:/{fileName}.flv', 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
                    file.write(data)  # 每次只写入data大小
                    size = len(data) + size
                    # 'r'每次重新从开始输出，end = ""是不换行
                    print("\r已经下载：" + int(size / content_size * 30) * "█" + " " + str(round(float(size / content_size) * 100, 1)) + "%", end="")
            end = time.time()
            print("\n总耗时:" + str(round(end - start)) + "秒")
            break
        else:
            if index == 4:
                print('接口暂时无法访问, 请稍后重试')


# 循环所有地址
def re_all_episodes(episodes):
    for ele in episodes:
        downloadurl(ele['cid'], ele['bvid'], ele['share_copy'])


# 根据 season_id 返回所有集数的 bvid, cid
def get_all_episodes(media_id):
    headers['Host'] = 'api.bilibili.com'
    season_id = get_season_id(media_id)
    if season_id != 'False':
        url = 'https://api.bilibili.com/pgc/view/web/season?season_id=' + season_id
        for index in range(5):
            resp = session.get(url, headers=headers)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if data['code'] == 0:
                        episodes = data['result']['episodes']
                        return episodes
                except:
                    print('接口可能已经更改')
                    return 'False'
            else:
                if index == 4:
                    return 'False'


# 获取 番剧 的 season_id
def get_season_id(media_id):
    headers['Host'] = 'api.bilibili.com'
    url = 'https://api.bilibili.com/pgc/review/user?media_id=' + media_id
    for index in range(5):
        resp = session.get(url, headers=headers)
        if resp.status_code == 200:
            try:
                data = resp.json()
                season_id = str(data['result']['media']['season_id'])
                return season_id
            except:
                print('接口可能已经更改')
                return 'False'
        else:
            if index == 4:
                print('接口暂时无法访问, 请稍后重试')
                return 'False'


# 获取下载地址
def downloadurl(cid, bvid, title):

    print(f'正在下载: {title}')
    headers['Referer'] = 'https://www.bilibili.com/video/' + bvid

    url = 'https://api.bilibili.com/x/player/playurl?cid={0}&bvid={1}&qn={2}'
    durl = []   # 视频源地址
    for index in range(5):
        resp = session.get(url.format(cid, bvid, qn), headers=headers)
        if resp.status_code == 200:
            try:
                data = resp.json()
                durl = data['data']['durl']
                break
            except:
                print('该集需要会员才能下载')
                return
        else:
            if index == 4:
                print('接口暂时无法访问, 请稍后重试')
                return

    if not is_auto:   # 静默下载
        _durl = durl[0]['url']
        headers['Host'] = _durl[_durl.find('://') + 3:_durl.find('/upgcxcode')]
        for ele in durl:
            process(ele['url'], headers, title)
    else:   # 导出IDM文件
        with open('c:/download.ef2', 'a', encoding='utf-8') as f:
            for ele in durl:
                f.write('<\n')
                f.write(ele['url'] + '\n')
                f.write('referer: https://www.bilibili.com\n')
                f.write('>\n')
        return


# 返回番剧的aid, bvid, cid
def get_anime_data(url):
    headers['Host'] = 'api.bilibili.com'
    for index in range(5):
        resp = session.get(url, headers=headers)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data['code'] == 0:
                    # 如果是 ss 的形式, 只返回第一集
                    if url.rfind('season_id') != -1:
                        first_ep = data['result']['episodes'][0]
                        return first_ep['cid'], first_ep['bvid'], first_ep['share_copy']
                    for ele in data['result']['episodes']:
                        # single_ep = [ele['cid'], ele['bvid'], ele['share_copy']]
                        if ele['id'] == int(url[url.find('=')+1:]):
                            return ele['cid'], ele['bvid'], ele['share_copy']
                else:
                    if index == 4:
                        print('接口暂时无法访问, 请稍后重试')
            except:
                print('接口可能已经失效了')
                break
        else:
            if index == 4:
                print('接口暂时无法访问, 请稍后重试')


# 请求接口(普通视频)
def get_cid_data(url):
    # 修改因下载视频被更改的Host
    headers['Host'] = 'api.bilibili.com'
    for index in range(5):
        resp = session.get(url, headers=headers)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if data['code'] == 0:
                    aid = data['data']['aid']
                    bvid = data['data']['bvid']
                    cid = data['data']['cid']
                    title = data['data']['title']
                    return cid, bvid, title
            except:
                print('接口可能已经失效了')
                break
        else:
            if index == 4:
                print('接口暂时无法访问, 请稍后重试')


# 根据 av 号或 bv 号获取 cid 和视频标题
def get_cid(video_id):
    # 先判断是 aid 还是bvid
    if video_id[:2] == 'av':
        av_url = 'https://api.bilibili.com/x/web-interface/view?aid=' + video_id[2:]
        # print(av_url)
        return get_cid_data(av_url)
    elif video_id[:2] == 'ss':   # 只下载番剧第一集
        ss_url = 'https://api.bilibili.com/pgc/view/web/season?season_id=' + video_id[2:]
        return get_anime_data(ss_url)
    elif video_id[:2] == 'ep':   # 番剧非第一集
        ep_url = 'https://api.bilibili.com/pgc/view/web/season?ep_id=' + video_id[2:]
        return get_anime_data(ep_url)
    elif video_id[:2] == 'md':   # 下载番剧所有集数
        episodes = get_all_episodes(video_id[2:])
        if episodes != 'False':
            re_all_episodes(episodes)
    else:
        bvid_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + video_id
        # print(bvid_url)
        return get_cid_data(bvid_url)


def get_nav(cookies):
    url_login_status = 'https://api.bilibili.com/x/web-interface/nav'
    headers['cookie'] = cookies

    for index in range(5):
        resp = session.get(url_login_status, headers=headers)
        # print(resp.text)
        if resp.status_code == 200:
            if resp.json()['code'] == 0 and resp.json()['data']['isLogin'] is True:
                return True
            else:
                return False
        else:
            if index == 4:
                return False  # 4 次都没有访问成功, 则返回失败


# 判断cookies是否有效
def login_status():
    if not os.path.exists('c:/bilicookie.txt'):
        with open('c:/bilicookie.txt', 'w') as f:
            cookies = input('请添加cookies: ')
            f.write(cookies)
        return get_nav(cookies)
    else:
        with open('c:/bilicookie.txt', 'r') as f:
            cookies = f.readline()
        return get_nav(cookies)


# 登录后开始下载
def start():
    global is_auto, qn
    video_ids = []
    for index in range(5):
        video_id = input('请输入av号或bv号(需要携带av和BV|支持多个视频|支持整部番剧下载<md开头>|单集番剧下载<ep开头或ss开头>,以英文逗号<,>分隔): ')
        video_ids.clear()
        for ele in video_id.split(','):
            try:
                pattern = re.search(r'av[0-9]+|BV1\w+|ep[0-9]+|ss[0-9]+|md[0-9]+', ele)
                video_id = pattern.group(0)
                video_ids.append(video_id)
            except:
                if index == 4:
                    print('输入次数过多, 程序结束运行')
                    return  # 退出方法
                print('输入的ID无效, 请重新输入')
                break
        else:
            break  # 输入无误时退出两层循环, 然后下一步分辨率...
    quality = input('视频分辨率(1.1080p 2.720p 3.480p | 默认为720p): ')
    if quality == '1' or quality == '1080p' or quality == '1080':
        qn = '80'
    elif quality == '3' or quality == '480p' or quality == '480':
        qn = '32'
    else:
        qn = '64'
    download = input('是否静默下载(1. 否 2. 是 | 默认为否, 将导出IDM下载文件): ')
    if download == '2' or download == '是':
        is_auto = False
    else:
        is_auto = True  # 导出IDM文件
    # print(video_ids)
    for ele in video_ids:
        if ele[:2] == 'md':  # 如果是下载所有剧集
            get_cid(ele)
        else:
            cid, bvid, title = get_cid(ele)
            downloadurl(cid, bvid, title)


# 主程序
def main():
    if login_status():  # cookies 有效
        start()
    else:
        print('cookie无效')


if __name__ == '__main__':
    main()
