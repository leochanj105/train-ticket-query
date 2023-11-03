from common import *
import json
import requests
from common import *
import sys

if __name__ == '__main__':
    aid = sys.argv[1]
    token = sys.argv[2]
    orderId = sys.argv[3]
    canceltime, cancelres = cancel(aid, token, orderId)
    with open("time_cancel", "a") as f:
        f.write(str(canceltime)+"\n")