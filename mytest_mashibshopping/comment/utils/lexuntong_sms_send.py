import urllib.request
import urllib
import json
import hashlib
import time

#参数配置

url = "http://www.lokapi.cn/smsUTF8.aspx"

rece = "json"
username = "13229452942"
password = "13229452942"
tokenYZM = "14891f2f"
#参数
templateid = "A072FC32"
def MD5(str):
    m = hashlib.md5()
    m.update(str.encode(encoding='UTF-8'))
    return m.hexdigest().upper()
    #密码加密
passwd = MD5(password)
#时间戳
def send_sm(phone,code):
    param = phone+"|"+code
    ticks =int(time.time() * 1000)
    #构造发送主体
    dict = {"action": "sendtemplate", "username": username,"password": passwd, "token": tokenYZM, "timestamp": ticks}
    body = "action=sendtemplate&username={username}&password={password}&token={token}&timestamp={timestamp}".format(username=username,password=passwd,token=tokenYZM,timestamp=ticks)
    sign = MD5(body)
    dict["sign"] = sign
    dict["rece"] = rece
    dict["templateid"] = templateid
    dict["param"] = param
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    data = urllib.parse.urlencode(dict).encode('utf-8')
    request = urllib.request.Request(url, data, headers)
    text_rece = urllib.request.urlopen(request).read().decode('utf-8')
    print("文字短信接收数据："+ text_rece)


    return text_rece


