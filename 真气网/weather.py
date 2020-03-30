import execjs
import requests
import json
from settings import *
from httputils import getheaders

"""
1.数据来源: https://www.aqistudy.cn
"""


class weather(object):

    def __init__(self):
        self.encodeparamfuncname = encodeparamfuncname
        self.decodedatafuncname = decodedatafuncname
        self.paramname = paramname
        self.method = method
        self.city = city
        self.session = requests.session()
        self.session.headers = getheaders()

    # 获得某城市空气质量情况
    def getweatherdata(self):
        weatherurl = "https://www.aqistudy.cn/apinew/aqistudyapi.php"  # ajax 请求地址(解密js代码后可见)
        # 请求参数
        datas = {
            self.paramname: self.getparams()   # 加密后的参数
        }
        data = self.session.post(weatherurl, data=datas).text  # 返回加密后的数据
        result = json.loads(self.decryptdata(data))
        print(result)

    # 获取加密后的参数
    def getparams(self):
        with open('wether.js', 'r', encoding='utf-8') as fp:
            line = fp.read()
        ctx = execjs.compile(line)  # 读取js中的函数。
        # 执行自定义函数getPostParamCode
        result = ctx.call('getPostParamCode', self.method, self.city)
        return result

    # 解密返回的data
    def decryptdata(self, data):
        with open('wether.js', 'r', encoding='utf-8') as fp:
            line = fp.read()
        ctx = execjs.compile(line)  # 再次读取一遍js文件， 要调用其中的解密函数。
        result = ctx.call(decodedatafuncname, data)   # 调用解密函数, 解析返回data数据
        return result  # 方法10分钟变一次


if __name__ == '__main__':
    weather().getweatherdata()

