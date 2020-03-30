import requests
import json

url = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=596907446235&sellerId=575351139&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,page,originalPrice,tradeContract&callback=onSibRequestSuccess'

userAgent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
cookie = '你的淘宝cookies'
headers = {
    'Host': 'detailskip.taobao.com',
    'Referer': 'https://item.taobao.com/item.htm?spm=a230r.1.14.22.4d6630beTtK7XI&id=596907446235&ns=1&abbucket=13',
    'User-Agent': userAgent,
    'cookie': cookie
}

session = requests.session()

resp = session.get(url, headers=headers).text
result = resp[resp.find('Success({')+8:-2]
str_to_dict = json.loads(result)
print(str_to_dict)
