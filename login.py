from common import *
import json
import requests
from common import *
logininfo = {"email":"fdse_microservices@163.com", "password":"DefaultPassword", "verificationCode" :"abcd"}
cookies = {"YsbCaptcha" : "abcd"}
res = requests.post("http://"+  loginaddr +":12342/login", json = logininfo, cookies = cookies)
resobj = json.loads(res.text)
aid = None
if 'account' in resobj:
    aid = resobj['account']['id']
    print(aid)
else:
    print(resobj)
if 'token' in resobj:
    token = resobj['token']
    print(token)
else:
    print(resobj)

#print(token)
