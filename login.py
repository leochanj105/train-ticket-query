from common import *
import json
import requests
from common import *
logininfo = {"email":"fdse_microservices@163.com", "password":"DefaultPassword", "verificationCode" :"abcd"}
res = requests.post("http://"+  loginaddr +":12342/login", json = logininfo)
resobj = json.loads(res.text)

aid = resobj['account']['id']
token = resobj['token']

print(aid)
print(token)
