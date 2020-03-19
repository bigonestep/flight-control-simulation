from urllib.request import urlopen
import json
from pprint import pprint
# u=urlopen('https://www.baidu.com/').read() #get all content on url page
u1=urlopen('https://www.baidu.com/')
print(u1.info()) #get header information from remote server
# print(u1.getcode())#get status code
# print(u1.geturl())#get request url