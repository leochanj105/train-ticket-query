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
warmthds = 20
warmreqs = 100
cutoff = 100
def runmtres(nthds, aid, token, nreqs, trecs, orderids, tripids):
    if trecs == None:
        trecs = [[] for i in range(nthds)]
    starts = [0.0] * nthds
    ends = [0.0] * nthds
    threads = []
    for i in range(nthds):
        t = Thread(name = "thread_" + str(i), target=runpres, args = (aid, token, nreqs,trecs[i] ,orderids[i], tripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(nthds):
        t = threads[i]
        t.join()
    return starts, ends
def runmtpay(nthds, aid, token, trecs, orderids, tripids):
    if trecs == None:
        trecs = [[] for i in range(nthds)]
    starts = [0.0] * nthds
    ends = [0.0] * nthds
    threads = []
    for i in range(nthds):
        t = Thread(name = "thread_" + str(i), target=runpay, args = (aid, token, trecs[i], orderids[i], tripids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(nthds):
        t = threads[i]
        t.join()
    return starts, ends

def runmtcancel(nthds, aid, token, trecs, orderids):
    if trecs == None:
        trecs = [[] for i in range(nthds)]
    starts = [0.0] * nthds
    ends = [0.0] * nthds
    threads = []
    for i in range(nthds):
        t = Thread(name = "thread_" + str(i), target=runcancel, args = (aid, token, trecs[i], orderids[i], starts, ends, i))
        threads.append(t)
        t.start()
    for i in range(nthds):
        t = threads[i]
        t.join()
    return starts, ends


def calcDuration(starts, ends):
    endsexclude = np.array(ends)
    startsexclude = np.array(starts)
    
    endsexclude = endsexclude[endsexclude!=0]
    startsexclude = startsexclude[startsexclude!=0]
    if endsexclude.shape[0] == 0 or startsexclude.shape[0] == 0:
        return 0
    return max(endsexclude) - min(startsexclude) 
 
def runmt(num_threads, nreq, aid, token, isWarmup=False):
    allpretimes = [[] for i in range(num_threads)]
    allpaytimes = [[] for i in range(num_threads)]
    allcanceltimes = [[] for i in range(num_threads)]
    allorderids = [[] for i in range(num_threads)]
    #warmuporderids = [[] for i in range(warmthds)]
    alltripids = [[] for i in range(num_threads)]
    #warmuptripids = [[] for i in range(warmthds)]
    #print("warming up reserve..")
    #runmtres(warmthds, aid, token, warmreqs, None, warmuporderids, warmuptripids)
    #print("warming up reserve finished..")

    print("reserving")
    starts, ends = runmtres(num_threads, aid, token, nreq, allpretimes, allorderids, alltripids)
    print("reserved: ", sum([len(l) for l in allorderids]))
    preduration = calcDuration(starts, ends)
    time.sleep(5)

    #print("warming up pay..")
    #runmtpay(warmthds, aid, token, None, warmuporderids, warmuptripids)
    #print("warming up pay finished..")

    print("paying")
    starts, ends = runmtpay(num_threads, aid, token, allpaytimes, allorderids, alltripids)
    payduration = calcDuration(starts, ends) 
    
    time.sleep(5)
    #print("warming up cancel..")
    #runmtcancel(warmthds, aid, token, None, warmuporderids)
    #print("warming up cancel finished..")

    print("canceling")
    starts, ends = runmtcancel(num_threads, aid, token, allcanceltimes, allorderids)
    cancelduration = calcDuration(starts, ends)
    if isWarmup:
        return None, None, None, None, None, None
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
    
    goodpre = sum([len(l) for l in allpretimes])
    goodpay = sum([len(l) for l in allpaytimes])
    goodcancel = sum([len(l) for l in allcanceltimes])
    print(goodpre, preduration)
    print(goodpay, payduration)
    print(goodcancel, cancelduration)
    # actualtime = reqtime - 2*keepoff
    tpre = goodpre/preduration
    tpay = goodpay/payduration
    tcancel = goodcancel/cancelduration
    # print(np.size(allpretimes))
    return meanpre, meanpay, meancancel, tpre, tpay, tcancel

def runpres(aid, token, nreq, pretimes, orderids, tripids, starts, ends, idx):
    with requests.Session() as session:
        for i in range(nreq):
            if i == cutoff:
                starts[idx] = time.time()
            isother = False
            if isother:
                orderId = str(uuid.uuid4())
                tripId = "Z1234"
                tripids.append(tripId)
                pretime, preres = preserve_other(aid, token, orderId, tripId, session)
                if pretime is not None and preres is not None and 'order' in preres and 'id' in preres['order']:
                        if i >= cutoff and i < nreq-cutoff:
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
                        if i >= cutoff and i < nreq-cutoff:
                            pretimes.append(pretime)
                        orderId = preres['order']['id']
                        orderids.append(orderId)
                        if alwaysPrint:
                            print(preres)
                else:
                    print("reached after res...", pretime, preres)
            if i == (nreq - cutoff - 1):   
                ends[idx] = time.time()
    
def runpay(aid, token, paytimes, orderids, tripids, starts, ends, idx):
    with requests.Session() as session:
        nreq = len(orderids)
        for i in range(nreq):
            if i == cutoff:
                starts[idx] = time.time()
            paytime, payres = pay(aid, token, orderids[i], tripids[i], session)
            if paytime is not None and payres == True:
                if i >= cutoff and i < nreq-cutoff:
                    paytimes.append(paytime)
                if alwaysPrint:
                    print(payres)
            else:
                print("reached after pay...", paytime, payres)
            if i == (nreq - cutoff - 1):
                ends[idx] = time.time()

def runcancel(aid, token, canceltimes, orderids, starts, ends, idx):
    with requests.Session() as session:
        nreq = len(orderids)
        for i in range(nreq):
            if i == cutoff:
                starts[idx] = time.time()
            canceltime, cancelres = cancel(aid, token, orderids[i], session)
            if canceltime is not None and cancelres is not None and cancelres['status'] == True:    
                if i >= cutoff and i < nreq-cutoff:
                    canceltimes.append(canceltime)
                if alwaysPrint:
                    print(cancelres)
            else:
                print("reached after cancel...", canceltime, cancelres)
            if i == (nreq - cutoff - 1):
                ends[idx] = time.time()
            # print(cancelres)
    


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
        runmt(warmthds, warmreqs, aid, token, isWarmup=True)
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
