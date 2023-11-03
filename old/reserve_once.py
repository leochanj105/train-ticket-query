from common import *
import json
import requests
from common import *
import sys

if __name__ == '__main__':
    aid = sys.argv[1]
    token = sys.argv[2]
    pretime, preres = preserve(aid, token, "G1234")
    orderId = None
    if preres is not None:
        if 'order' in preres:
            if preres['order'] is not None:
                orderId = preres['order']['id']

    with open("time_reserve", "a") as f:
        f.write(str(pretime)+"\n")
    print(orderId)