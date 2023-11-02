import json
import requests
import time
import uuid
import numpy as np
from random import random
from threading import Thread, Barrier
import sys
timeout = 60
keepoff = 0
orderaddr = "node3.throughput.lumos-pg0.utah.cloudlab.us"
orderotheraddr = "node3.throughput.lumos-pg0.utah.cloudlab.us"
canceladdr = "node3.throughput.lumos-pg0.utah.cloudlab.us"
payaddr = "node3.throughput.lumos-pg0.utah.cloudlab.us"
presaddr = "node2.throughput.lumos-pg0.utah.cloudlab.us"
presotheraddr = "node2.throughput.lumos-pg0.utah.cloudlab.us"
loginaddr = "node3.throughput.lumos-pg0.utah.cloudlab.us"



date = time.strftime("%Y-%m-%d", time.localtime(time.time() + 24*3600))


def mean(arr):
    res = None
    if len(arr) > 0:
        res = sum(arr) / len(arr)
    else:
        res = 0
    return res

def getorder(aid, token, orderId):
    getInfo = {"orderId": orderId}
    cookies = {'loginId': aid, 'loginToken':token}
    start = time.time()
    res = requests.post("http://"+ orderaddr + ":12031/order/getById", json = getInfo, cookies=cookies, timeout=timeout)
    elapsed = time.time() - start
    return elapsed, json.loads(res.text)

def getother(aid, token, orderId):
    getInfo = {"orderId": orderId}
    cookies = {'loginId': aid, 'loginToken':token}
    start = time.time()
    res = requests.post("http://" + orderotheraddr + ":12032/orderOther/getById", json = getInfo, cookies=cookies, timeout=timeout)
    elapsed = time.time() - start
    return elapsed, json.loads(res.text)


def preserve_other(aid, token, orderId, tripId, session):
    orderTicketsInfoWithOrderId = {"contactsId":"aded7dc5-06a7-4503-8e21-b7cad7a1f386",
                                   "tripId":tripId,
                                   "seatType":2,
                                   "date": date,
                                   "from":"Shang Hai",
                                   "to":"Nan Jing",
                                   "orderId":orderId}
    cookies = {'loginId': aid, 'loginToken':token}
    # print(orderTicketsInfoWithOrderId)
    start = time.time()
    try:
        preserveres = session.post("http://" + presotheraddr + ":14569/preserveOther", json = orderTicketsInfoWithOrderId, cookies=cookies, timeout=timeout)
        elapsed = time.time() - start
        preservejson = json.loads(preserveres.text)
        return elapsed, preservejson
    except requests.exceptions.Timeout as e:
        print(e)
    return None,None

def preserve(aid, token, tripId, session):
    orderTicketsInfoWithOrderId = {"contactsId":"aded7dc5-06a7-4503-8e21-b7cad7a1f386",
                                   "tripId":tripId,
                                   "seatType":2,
                                   "date": date,
                                   "from":"Su Zhou",
                                   "to":"Shang Hai"}
    cookies = {'loginId': aid, 'loginToken':token}
    # print(orderTicketsInfoWithOrderId)
    start = time.time()
    try:
        preserveres = session.post("http://" + presaddr + ":14568/preserve", json = orderTicketsInfoWithOrderId, cookies=cookies, timeout=timeout)
        elapsed = time.time() - start
        preservejson = json.loads(preserveres.text)
        return elapsed, preservejson
    except requests.exceptions.Timeout as e:
        print(e)
    except Exception as e2:
        print("In reserve")
        print(e2)
        
    return None, None

def pay(aid, token, orderId, tripId, session):
    paymentInfo = {"orderId": orderId,
                   "tripId": tripId}
    cookies = {'loginId': aid, 'loginToken':token}
    start = time.time()
    try:
        res = session.post("http://" + payaddr + ":18673/inside_payment/pay", json = paymentInfo, cookies=cookies, timeout=timeout)
        elapsed = time.time() - start
        return elapsed, json.loads(res.text) 
    except requests.exceptions.Timeout as e:
        print(e)
    except Exception as e2:
        print("In pay")
        print(e2)
    return None, None
    
    
    
    
def cancel(aid, token, orderId, session):
    cancelInfo = {"orderId": orderId}
    cookies = {'loginId': aid, 'loginToken':token}
    start = time.time()
    try:
        res = session.post("http://" + canceladdr + ":18885/cancelOrder", json = cancelInfo, cookies=cookies, timeout=timeout)
        elapsed = time.time() - start
        return elapsed, json.loads(res.text)
    except requests.exceptions.Timeout as e:
        print(e)
    except Exception as e2:
        print("In cancel")
        print(e2)
    return None, None
