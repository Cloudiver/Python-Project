import smtplib
from email.mime.text import MIMEText

"""
发送邮件
"""
def email():

    sender = ''      # 填写发件人邮箱
    pwd = ''    # 第三方登录客户端授权码
    receiver = ''     # 填写收件人邮箱

    message = MIMEText("你好，网站有内容更新，请及时查看", "plain", 'utf-8')
    # 三个参数：第一个为文本内容，第二个为plain设置文本格式，第三个为utf-8设置编码
    message['From'] = "范 <xxxx123@126.com>"   # 发件人信息
    message['To'] = "fan <ooooo456@qq.com>"   # 收邮人邮箱信息

    subject = "网站有内容更新"
    # 邮件主题
    message["Subject"] = subject

    try:
        # 使用非本地服务器，需要建立ssl连接
        smtpObj = smtplib.SMTP_SSL("smtp.126.com", 465)   # 发件服务器地址和端口, 需要查看邮箱的帮助文档
        # 发件箱邮件服务器
        smtpObj.login(sender, pwd)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error：无法发送邮件.Case:%s" % e)
