import json
import requests
import time
import uuid
import numpy as np
from random import random
from threading import Thread, Barrier
import sys
import os
from common import *
# num_threads = 2
# num_reqs_per_thread = 1
# reqtime = 5


alwaysPrint=False

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

    starts = [0.0] * num_threads
    ends = [0.0] * num_threads
    print("reserving")
    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runpres, args = (aid, token, nreq, allpretimes[i], allorderids[i], alltripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()

    endsexclude = np.array(ends)
    startsexclude = np.array(starts)
    endsexclude = endsexclude[endsexclude!=0]
    startsexclude = startsexclude[startsexclude!=0]
    preduration = max(endsexclude) - min(startsexclude) 
    print("reserved: ", sum([len(l) for l in allorderids]))

    starts = [0.0] * num_threads
    ends = [0.0] * num_threads

    print("paying")
    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runpay, args = (aid, token, allpaytimes[i], allorderids[i], alltripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()
    endsexclude = np.array(ends)
    startsexclude = np.array(starts)
    endsexclude = endsexclude[endsexclude!=0]
    startsexclude = startsexclude[startsexclude!=0]
    payduration = max(endsexclude) - min(startsexclude) 
    
    print("canceling")
    starts = [0.0] * num_threads
    ends = [0.0] * num_threads
    threads = []
    for i in range(num_threads):
        t = Thread(name = "thread_" + str(i), target=runcancel, args = (aid, token, allcanceltimes[i], allorderids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(num_threads):
        t = threads[i]
        t.join()


    endsexclude = np.array(ends)
    startsexclude = np.array(starts)
    endsexclude = endsexclude[endsexclude!=0]
    startsexclude = startsexclude[startsexclude!=0]
    cancelduration = max(endsexclude) - min(startsexclude) 

    #print(allpaytimes)
    #print(allcanceltimes)
    meanpre = 0
    meanpay = 0
    meancancel = 0
    try:
        meanpre = np.mean(sum(allpretimes, []))
    except Exception as e:
        print("meanpre exception")
        print(e)
    try:
        meanpay = np.mean(sum(allpaytimes, []))
    except Exception as e:
        print("meanpay exception")
        print(e)
    
    try:
        meancancel = np.mean(sum(allcanceltimes, []))
    except Exception as e:
        print("meancancel exception")
        print(e)
    
    # actualtime = reqtime - 2*keepoff
    tpre = np.size(allpretimes)/preduration
    tpay = np.size(allpaytimes)/payduration
    tcancel = np.size(allcanceltimes)/cancelduration
    # print(np.size(allpretimes))
    return meanpre, meanpay, meancancel, tpre, tpay, tcancel

def runpres(aid, token, nreq, pretimes, orderids, tripids, starts, ends, idx):
    with requests.Session() as session:
        starts[idx] = time.time()
        for i in range(nreq):
            isother = False
            if isother:
                orderId = str(uuid.uuid4())
                tripId = "Z1234"
                tripids.append(tripId)
                pretime, preres = preserve_other(aid, token, orderId, tripId, session)
                if pretime is not None and preres is not None and 'order' in preres and 'id' in preres['order']:
                        pretimes.append(pretime)
                        orderId = preres['order']['id']
                        orderids.append(orderId)
                        if alwaysPrint:
                            print(preres)
                else:
                    print("reached after res...", pretime, preres)

            else:
                tripId = "G1234"
                tripids.append(tripId)
                pretime, preres = preserve(aid, token, tripId, session)
                if pretime is not None and preres is not None and 'order' in preres and 'id' in preres['order']:
                        pretimes.append(pretime)
                        orderId = preres['order']['id']
                        orderids.append(orderId)
                        if alwaysPrint:
                            print(preres)
                else:
                    print("reached after res...", pretime, preres)
        ends[idx] = time.time()
    
def runpay(aid, token, paytimes, orderids, tripids, starts, ends, idx):
    with requests.Session() as session:
        starts[idx] = time.time()
        for i in range(len(orderids)):
            paytime, payres = pay(aid, token, orderids[i], tripids[i], session)
            if paytime is not None and payres == True:
                paytimes.append(paytime)
                if alwaysPrint:
                    print(payres)
            else:
                print("reached after pay...", paytime, payres)
        ends[idx] = time.time()

def runcancel(aid, token, canceltimes, orderids, starts, ends, idx):
    with requests.Session() as session:
        starts[idx] = time.time()
        for i in range(len(orderids)):
            canceltime, cancelres = cancel(aid, token, orderids[i], session)
            if canceltime is not None and cancelres is not None and cancelres['status'] == True:
                canceltimes.append(canceltime)
                if alwaysPrint:
                    print(cancelres)
            else:
                print("reached after cancel...", canceltime, cancelres)
            # print(cancelres)
        ends[idx] = time.time()
    


if __name__ == '__main__':
    num_threads = int(sys.argv[1])
    nreqpt = int(sys.argv[2])
    dirname = sys.argv[3]
    aid = sys.argv[4]
    token = sys.argv[5]
    # keepoff = float(sys.argv[3])

    #logininfo = {"email":"fdse_microservices@163.com", "password":"DefaultPassword", "verificationCode" :"abcd"}
    #res = requests.post("http://"+  loginaddr +":12342/login", json = logininfo)
    #resobj = json.loads(res.text)
    #print(resobj)
    #aid = resobj['account']['id']
    #token = resobj['token']
    
    
    if num_threads <= 0:
        #warmup
        print("warmingup...")
        runmt(20, nreqpt, aid, token)
        print("warm finished")
        exit(0)

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
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(dirname+"/meanpres_"+str(num_threads), "a") as f:
        for data in meanpres:
            f.write(str(data)+"\n")
    with open(dirname+"/meanpay_"+str(num_threads), "a") as f:
        for data in meanpays:
            f.write(str(data)+"\n")
    with open(dirname+"/meancancel_"+str(num_threads), "a") as f:
        for data in meancancels:
            f.write(str(data)+"\n")
    with open(dirname+"/tpres_"+str(num_threads), "a") as f:
        for data in tpres:
            f.write(str(data)+"\n")
    with open(dirname+"/tpays_"+str(num_threads), "a") as f:
        for data in tpays:
            f.write(str(data)+"\n")
    with open(dirname+"/tcancels_"+str(num_threads), "a") as f:
        for data in tcancels:
            f.write(str(data)+"\n")

    # main()
