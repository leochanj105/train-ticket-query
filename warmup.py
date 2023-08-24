import json
import requests
import time
import uuid
import numpy as np
from random import random
from threading import Thread, Barrier
import sys
from common import *
from req import runmt

if __name__ == '__main__':
    aid = sys.argv[1]
    token = sys.argv[2]
    print("warmingup...")
    runmt(20, 20, aid, token)
    print("warm finished")