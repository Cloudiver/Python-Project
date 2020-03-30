# coding=utf-8
"""
1.百度接口获取疫情信息: https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1
2.网易新闻接口: https://wp.m.163.com/163/page/news/virus_report/index.html
"""
import requests
import json
import time
import csv


# 通过百度接口获取
def getncovmsg():
    unixtimestamp = time.localtime(int(time.time()) - 86400)  # localtime() 输出结构体时间
    month = time.strftime('%m', unixtimestamp).lstrip('0') + '月'
    day = time.strftime('%d', unixtimestamp).lstrip('0') + '日'
    date = month + day

    session = requests.session()
    result = session.get('https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1')
    res = result.text
    res = res[res.find('{\"page\"'):res.find('</script><script>var')]  # 返回字符串
    foreignncov = json.loads(res)['component'][0]['summaryDataOut']
    chinancov = json.loads(res)['component'][0]['summaryDataIn']
    wuhanncovmsg = json.loads(res)['component'][0]['caseList'][-1]['subList'][-6]
    confirmedRelative = wuhanncovmsg['confirmedRelative']  # 新增确诊
    confirmed = wuhanncovmsg['confirmed']  # 总共确诊
    # python3.6以上
    # return f'{date}\n' \
    #       f'国内新增确诊{chinancov["confirmedRelative"]}例, 总共确诊{chinancov["confirmed"]}例\n' \
    #       f'武汉新增确诊{confirmedRelative}例, 总共确诊{confirmed}例\n' \
    #       f'国外总共确诊{foreignncov["confirmed"]}例'

    # python3.6以下
    return date + '\n' \
           + '国内新增确诊' + chinancov["confirmedRelative"] + '例, 总共确诊' + chinancov["confirmed"] + '例\n' \
           + '武汉新增确诊' + confirmedRelative + '例, 总共确诊' + confirmed + '例\n' \
           + '国外总共确诊' + foreignncov["confirmed"] + '例'


# 网易接口信息
"""
1. 历时总数据(1月21~): https://c.m.163.com/ug/api/wuhan/app/data/list-total
2. 根据区域查询历时数据: https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=440000
"""
def netease():
    totalurl = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    session = requests.session()
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    resp = session.get(totalurl, headers=header).text
    data = json.loads(resp)  # 返回字典形式
    # 国内历史数据
    chinaDayList = data['data']['chinaDayList']  # 返回列表
    for ele in chinaDayList:
        print("%s | %s" % (ele["date"], ele["total"]["confirm"]))
    # 获取区域ID
    children = data['data']['areaTree'][0]['children']
    with open("e:\\nCov.csv", "a", newline='') as f:
        for i, ele in enumerate(children):
            # 获取ID后就可以根据ID查询各省份历史数据
            provencedata = getprovencedatabyid(f'{ele["id"]}')
            for j, index in enumerate(provencedata["data"]["list"]):
                fieldnames = ['ID', '省份', '日期', '新增确诊', '确诊', '死亡', '治愈']
                if i == 0 and j == 0:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                writer.writerow({'ID': ele["id"], '省份': ele["name"], '日期': index["date"], '新增确诊': index["today"]["confirm"],
                                '确诊': index['total']['confirm'], '死亡': index["total"]["dead"], '治愈': index["total"]["heal"]})
            print(time.strftime('%Y-%m-%d %H:%M:%S') + f' {ele["name"]}数据写入完成')
        print("------------")
        print(time.strftime('%Y-%m-%d %H:%M:%S') + "全部省份数据写入完成")
    """
    if i == 0 and j == 0:
        print("ID", "|", "省份", "|", "日期", "|", "新增确诊", "|", "确诊", "|", "死亡", "|", "治愈")
    print(ele["id"], "|", ele["name"], "|", index["date"], "|", index["today"]["confirm"], "|", index['total']['confirm'],
          index["total"]["dead"], "|", index["total"]["heal"])
    """


def getprovencedatabyid(areaid):
    areadataurl = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='
    session = requests.session()
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
    }
    data = json.loads(session.get(f'{areadataurl}{areaid}', headers=header).text)
    return data


if __name__ == "__main__":
    getncovmsg()
    # netease()