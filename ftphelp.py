import MDM
import MOD 
import sys

def MDM_waitfor(value, timeout):
    res = ''
    found = -1
    b = MOD.watchdogReset()
    start = MOD.secCounter()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            print res   
            return found
    print res   
    return found
def Wait(sec):
    timer = MOD.secCounter()
    timerstop = timer + sec
    b = MOD.watchdogReset()
    while timer < timerstop:
        timer = MOD.secCounter()
def MDM_receive(timeout):
    res = ''
    start = MOD.secCounter()
    b = MOD.watchdogReset()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
    return res	