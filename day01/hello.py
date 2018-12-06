import urllib.request
from urllib import request,parse


url = "http://2018.sina.com.cn/"
#
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",\
           "Host": "2018.sina.com.cn", }
# 需要传参数使用到
dict = {
    "name": "Question"
}
# 对参数进行处理
data = bytes(parse.urlencode(dict), encoding="utf8")
req = request.Request(url=url, data=data, headers=headers, method="GET")
response = request.urlopen(req)
print(response.read().decode("utf-8"))


url = "http://2018.sina.com.cn/"
response = urllib.request.urlopen(url, timeout=1)  # 设置超时时间timeout=1
html = response.read().decode("utf-8")
aa = response.getheaders()
bb = response.status
print(html, aa, bb)
