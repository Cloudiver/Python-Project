import requests
import time
from lxml import etree
import smtplib
from email.mime.text import MIMEText

"""
云大研招网通知更新
借助linux crontab 定时任务实现
"""


# 清洗列表
def format_str(list_str):
    listap = []  # 第一页列表
    for str in list_str:
        str_format = str.replace("\r\n", "").replace(" ", "").rstrip()
        if str_format != '':
            listap.append(str_format)
    return listap


def email(noticetext):
    sender = ''      # 填写发件人
    pwd = ''    # 第三方登录客户端授权码
    receiver = ''     # 填写收件人

    message = MIMEText(noticetext, 'plain', 'utf-8')
    # 三个参数：第一个为文本内容，第二个为plain设置文本格式，第三个为utf-8设置编码
    message['From'] = "范 <0000@126.com>"
    message['To'] = "fan <00000@qq.com>"

    subject = "云大研招网通知更新"
    # 邮件主题
    message['Subject'] = subject

    try:
        # 使用非本地服务器，需要建立ssl连接
        smtpObj = smtplib.SMTP_SSL("smtp.126.com", 465)
        # 发件箱邮件服务器
        smtpObj.login(sender, pwd)
        smtpObj.sendmail(sender, receiver, message.as_string())
        # print("邮件发送成功")
        # 输出log
        with open("/home/g/notice.log", "a") as f2:
            f2.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "邮件发送成功\n")
    except smtplib.SMTPException as e:
        # print("Error：无法发送邮件.Case:%s" % e)
        # 输出错误log
        with open("/home/g1476763739/notice.log", "a") as f3:
            f3.write(time.strftime("%Y-%m-%d %H:%M:%S ") + "Error：无法发送邮件.Case:%s\n" % e)


url = 'http://www.grs.ynu.edu.cn/zsgz/qrzssyjs.htm'
content = requests.get(url).content
html = etree.HTML(content)
toptitle = html.xpath("//div[@id='con_list']/ul/li/a/font/text()")  # 置顶通知
title2 = html.xpath("//div[@id='con_list']/ul/li/a/text()")
path = html.xpath("//div[@id='con_list']/ul/li/a/@href")


new_titlelist = []  # 新建一个列表保存新的信息

# 处理置顶通知
toptitlelen = len(format_str(toptitle))
# print(format_str(toptitle))
for i, toptitlelist in enumerate(format_str(toptitle)):
    topnum = toptitlelist.rfind("[") + 1
    if time.strftime('%m-%d') == toptitlelist[topnum:-1]:
        new_titlelist.append(toptitlelist)  # 添加标题
        new_titlelist.append("http://www.grs.ynu.edu.cn" + path[i].replace("..", ""))


# 取出列表中当天的通知(非置顶通知)
for index, liststr in enumerate(format_str(title2)):   # 遍历所有信息, 并获取索引
    num = liststr.rfind("[") + 1
    if time.strftime('%m-%d') == liststr[num:-1]:  # 根据今天的日期判断是否有文章发布
        new_titlelist.append(liststr)
        new_titlelist.append("http://www.grs.ynu.edu.cn" + path[toptitlelen + index].replace("..", ""))


# print(new_titlelist)  # 最后获取到当天更新的通知
# 通知列表发邮件
# 列表转字符串
updatenotice = ''
for index2, text in enumerate(new_titlelist):
    temp = ''
    if index2 % 2 != 0:  # 奇数
        temp = new_titlelist[index2 - 1] + "  " + new_titlelist[index2] + "\n"
    updatenotice = updatenotice + temp
if updatenotice != '':
    email(updatenotice)  # 发送邮件通知

