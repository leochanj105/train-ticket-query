import os
import uuid


def ToUUID(h):
    msb = h[0:16]
    lsb = h[16:]
    msb = msb[14:16] + msb[12:14] + msb[10:12] + msb[8:10] + msb[6:8] + msb[4:6] + msb[2:4] + msb[0:2]
    lsb = lsb[14:16] + lsb[12:14] + lsb[10:12] + lsb[8:10] + lsb[6:8] + lsb[4:6] + lsb[2:4] + lsb[0:2]
    h = msb + lsb
    return uuid.UUID(h)


UUIDs = []
with open("tmp/ids") as f:
    for line in f:
        print(ToUUID(line.strip()))
