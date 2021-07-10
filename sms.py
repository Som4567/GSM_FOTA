import MDM
import MOD 
import sys

FTPSERVER_ADDR = ''
FTPUSERNAME = ''
FTPPASSWORD = ''
DirName = ''
FILENAME = ''

def delsms():
    b = MOD.watchdogReset()
    print 'deleting msg'
    MDM.send('at+cmgd=1,4\r', 0)
    res = MDM_waitfor('OK',20)
    if(res == -1):
        print 'error deleting sms'
    print res

def SmsSetup():
    b = MOD.watchdogReset()
    a = MDM.send('AT+CMGF=1\r', 0)
    trovato = MDM_waitfor('OK', 10)
    a = MDM.send('AT+CNMI=2,1\r', 0)
    trovato = MDM_waitfor('OK', 10)
    a = MDM.send('AT+CLIP=1\r', 0)
    trovato = MDM_waitfor('OK', 10)

def LookforSMS(txt):
    b = MOD.watchdogReset()
    foundPos = -1
    strtxt = ''
    strd2 = ''
    strd3 = ''

    foundPos = txt.find('+CMGR:')
    if(foundPos != -1):
        strtxt = txt[foundPos+5:]
        print strtxt
    else:
        print 'error pos'
        return strtxt

    findendl = strtxt.rfind('"')
    if(findendl != -1):
        strd2 = strtxt[findendl+1:]
        print strd2
    else:
        print 'error endl'
        return strd2


    findok = strd2.find('OK')

    if(findok != -1):
        strd3 = strd2[:findok-2]
        print strd3
    else:
        print 'error: Ok not found looking for SMS'
        return strd2
    
    return strd3

def ExtractInfo(textSms):
# FOTA:ftp.innovations.com:test@innovations.com:TEST@1234:telit:FOTA_TEST.pyo:OK
    global FILENAME
    b = MOD.watchdogReset()
    global FTPSERVER_ADDR
    global FTPUSERNAME
    global FTPPASSWORD
    global DirName
    infoList = textSms.split(':')
    n = len(infoList)
    print 'text sms is ',textSms
    if n == 7 :
       FTPSERVER_ADDR = infoList[1].strip()
       FTPUSERNAME = infoList[2].strip()
       FTPPASSWORD = infoList[3].strip()
       DirName = infoList[4].strip()
       FILENAME = infoList[5].strip()
       print 'server info',FTPSERVER_ADDR, FTPUSERNAME, FTPPASSWORD,  DirName, FILENAME
       return 1
    else :
       delsms()
       return -1
	   
# waiting function
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

def MDM_receiveUntil(value,timeout):
    res = ''
    found = -1
    b = MOD.watchdogReset()
    start = MOD.secCounter()
    while (MOD.secCounter() - start < timeout):
        res = res + MDM.read()
        found = res.find(value)
        if(found != -1):
            return res
            
    return res

def main_sms():
   try :
      SmsSetup()   
      SMSindex = checkForFotaMessagePos()
      if SMSindex != '-1' and SMSindex != '' :
         cmgr = 'AT+CMGR=' + SMSindex + '\r'
         print 'cmgr output ',cmgr
         a = MDM.send(cmgr, 0)
         SMStext = MDM_receiveUntil('OK',10)
         print 'smstext',SMStext
         TxtSMS = LookforSMS(SMStext)
         print 'textsms', TxtSMS
         if(TxtSMS != ''):
            ret = ExtractInfo(TxtSMS)
            if ret == 1 :
               return 1
      return -1
   except Exception, e:
      print 'Got exce in sms'
      delsms()
      return -1

def checkForFotaMessagePos():
   SMSindex = '-1'
   b = MOD.watchdogReset()
   a = MDM.send('AT+CMGL="ALL"\r',5)   
   msgList = MDM_receiveUntil('OK',10)
   print msgList
   if msgList != '' :
      print 'msglist',msgList
      allMsgList = msgList.split('+CMGL') 
      listLen = len(allMsgList)
      if msgList.find('FOTA')!= -1 :   
         fotaMsgCounter = 0
         fotaMsg = ''
         for msg in allMsgList :
            if msg.find('FOTA') != -1 :
               fotaMsgCounter = fotaMsgCounter + 1
               fotaMsg = msg
               print 'fota msg is ',fotaMsg			  
         if fotaMsgCounter > 1 :
            delsms()
         else :
            c = fotaMsg.find(':') + 1
            d= fotaMsg.find(',')
            SMSindex = fotaMsg[c:d].strip()
            print 'smsindex is',SMSindex
            return SMSindex
      else :
         if listLen > 10 :
            print 'deleting unwanted sms'
            delsms()  
   return '-1'

print 'SMS imported'
