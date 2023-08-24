from common import *
import json
import requests
from common import *
import sys

if __name__ == '__main__':
    aid = sys.argv[1]
    token = sys.argv[2]
    orderId = sys.argv[3]
    paytime, payres = pay(aid, token, orderId, "G1234")
    with open("time_pay", "a") as f:
        f.write(str(paytime)+"\n")