import json
import requests
import time
import uuid
import numpy as np
from random import random
from threading import Thread, Barrier
import sys
from common import *
# num_threads = 2
# num_reqs_per_thread = 1
# reqtime = 5




def runmt(num_threads, nreq, aid, token):
    allpretimes = []
    allpaytimes = []
    allcanceltimes = []
    allorderids = []
    alltripids = []

    for i in range(num_threads):
        pretimes = []
        paytimes = []
        canceltimes = []
        orderids = []
        tripids = []
        allpretimes.append(pretimes)
        allpaytimes.append(paytimes)
        allcanceltimes.append(canceltimes)
        allorderids.append(orderids)
        alltripids.append(tripids)

    starts = [0] * num_threads
    ends = [0] * num_threads

    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runpres, args = (aid, token, nreq, allpretimes[i], allorderids[i], alltripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()
    preduration = max(ends) - min(starts) 

    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runpay, args = (aid, token, allpaytimes[i], allorderids[i], alltripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()
    payduration = max(ends) - min(starts) 

    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runcancel, args = (aid, token, allcanceltimes[i], allorderids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()
    cancelduration = max(ends) - min(starts) 


    meanpre = np.mean(allpretimes)
    meanpay = np.mean(allpaytimes)
    meancancel = np.mean(allcanceltimes)
    # actualtime = reqtime - 2*keepoff
    tpre = np.size(allpretimes)/preduration
    tpay = np.size(allpaytimes)/payduration
    tcancel = np.size(allcanceltimes)/cancelduration
    # print(np.size(allpretimes))
    return meanpre, meanpay, meancancel, tpre, tpay, tcancel

def runpres(aid, token, nreq, pretimes, orderids, tripids, starts, ends, idx):
    starts[idx] = time.time()
    for i in range(nreq):
        isother = False
        if isother:
            orderId = str(uuid.uuid4())
            tripId = "Z1234"
            tripids.append(tripId)
            pretime, preres = preserve_other(aid, token, orderId, tripId)
            if pretime is not None:
                pretimes.append(pretime)    
            if preres is not None:
                # orderId = preres['order']['id']
                orderids.append(orderId)
        else:
            tripId = "G1234"
            tripids.append(tripId)
            pretime, preres = preserve(aid, token, tripId)
            if pretime is not None:
                pretimes.append(pretime)
            if preres is not None:
                if 'order' in preres:
                  if preres['order'] is not None:
                    orderId = preres['order']['id']
                    orderids.append(orderId)
    ends[idx] = time.time()
    
def runpay(aid, token, paytimes, orderids, tripids, starts, ends, idx):
    starts[idx] = time.time()
    for i in range(len(orderids)):
        paytime, payres = pay(aid, token, orderids[i], tripids[i])
        if paytime is not None:
            paytimes.append(paytime)
    ends[idx] = time.time()

def runcancel(aid, token, canceltimes, orderids, starts, ends, idx):
    starts[idx] = time.time()
    for i in range(len(orderids)):
        canceltime, cancelres = cancel(aid, token, orderids[i])
        if canceltime is not None:
            canceltimes.append(canceltime)
        # print(cancelres)
    ends[idx] = time.time()
    


if __name__ == '__main__':
    num_threads = int(sys.argv[1])
    nreqpt = int(sys.argv[2])
    # keepoff = float(sys.argv[3])

    logininfo = {"email":"fdse_microservices@163.com", "password":"DefaultPassword", "verificationCode" :"abcd"}
    res = requests.post("http://"+  loginaddr +":12342/login", json = logininfo)
    resobj = json.loads(res.text)
    print(resobj)
    aid = resobj['account']['id']
    token = resobj['token']
    

    #warmup
    print("warmingup...")
    runmt(20, 5, aid, token)
    print("warm finished")

    meanpres = []
    meanpays = []
    meancancels = []
    tpres = []
    tpays = []
    tcancels = []
    # nreqpt = 5
    
    #print(nt)
    meanpre, meanpay, meancancel, tpre, tpay, tcancel = runmt(num_threads, nreqpt, aid, token)
    meanpres.append(meanpre)
    meanpays.append(meanpay)
    meancancels.append(meancancel)
    tpres.append(tpre)
    tpays.append(tpay)
    tcancels.append(tcancel)

    snt = str(num_threads)
    with open("meanpres_"+str(num_threads), "w") as f:
        for data in meanpres:
            f.write(str(data)+"\n")
    with open("meanpay_"+str(num_threads), "w") as f:
        for data in meanpays:
            f.write(str(data)+"\n")
    with open("meancancel_"+str(num_threads), "w") as f:
        for data in meancancels:
            f.write(str(data)+"\n")
    with open("tpres_"+str(num_threads), "w") as f:
        for data in tpres:
            f.write(str(data)+"\n")
    with open("tpays_"+str(num_threads), "w") as f:
        for data in tpays:
            f.write(str(data)+"\n")
    with open("tcancels_"+str(num_threads), "w") as f:
        for data in tcancels:
            f.write(str(data)+"\n")

    # main()
