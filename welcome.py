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
cutoff = 50
def runmtw(nthds, nreq, trecs):
    if trecs == None:
        trecs = [[] for i in range(nthds)]
    starts = [0.0] * nthds
    ends = [0.0] * nthds
    threads = []
    for i in range(nthds):
        t = Thread(name = "thread_" + str(i), target=runwelcome, args = (nreq, trecs[i], starts, ends, i))
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
 
def runmt(num_threads, nreq,isWarmup=False):
    allpaytimes = [[] for i in range(num_threads)]
    print("welcome")
    starts, ends = runmtw(num_threads, nreq, allpaytimes)
    payduration = calcDuration(starts, ends) 
    
    meanpay = 0

    try:
        meanpay = np.mean(sum(allpaytimes, []))
    except Exception as e:
        print("welcome exception")
        print(e)
    
    
    goodpay = sum([len(l) for l in allpaytimes])
    print(goodpay, payduration)
    # actualtime = reqtime - 2*keepoff
    tpay = goodpay/payduration
    # print(np.size(allpretimes))
    return meanpay, tpay
    
def runwelcome(nreq, wtimes, starts, ends, idx):
    with requests.Session() as session:
        for i in range(nreq):
            if i == cutoff:
                starts[idx] = time.time()
            paytime, payres = welcome(session)
            if paytime is not None:
                if i >= cutoff and i < nreq-cutoff:
                    wtimes.append(paytime)
                if alwaysPrint:
                    print(payres)
            else:
                print("reached after welcome...", paytime, payres)
            if i == (nreq - cutoff - 1):
                ends[idx] = time.time()


    


if __name__ == '__main__':
    num_threads = int(sys.argv[1])
    nreqpt = int(sys.argv[2])
    # keepoff = float(sys.argv[3])
    
    #logininfo = {"email":"fdse_microservices@163.com", "password":"DefaultPassword", "verificationCode" :"abcd"}
    #res = requests.post("http://"+  loginaddr +":12342/login", json = logininfo)
    #resobj = json.loads(res.text)
    #print(resobj)
    #aid = resobj['account']['id']
    #token = resobj['token']
    
    

    # nreqpt = 5
    
    #print(nt)
    runmt(num_threads, nreqpt)
