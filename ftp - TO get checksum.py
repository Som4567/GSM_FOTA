import MDM
import MOD 
import sys
import md5 
import ftphelp
FTPSERVER_ADDR1= ''
FTPUSERNAME1 = ''
FTPPASSWORD1 = ''
DirName1 = ''
datatosave1 = ''

def GetFTP(fileName,CheckSum,flag) :
    global FTPSERVER_ADDR 
    global FTPUSERNAME
    global FTPPASSWORD
    b = MOD.watchdogReset()
    global DirName
    noIp = 1
    timer = MOD.secCounter() 
    resftp = -1
    kcount = 0;
    while (noIp == 1  or resftp == -1 or retGetFTP == -1):
        a = MDM.send('AT+CREG?\r',5)
        if(MOD.secCounter() - timer >300 ):
           return -1
        b = MOD.watchdogReset()	
        kcount = kcount + 1		
        if kcount > 3  and noIp == 0:
            print 'IP BREAK'
            result = MDM.send('AT#SH=1\r', 5)
            res = ftphelp.MDM_waitfor('OK',2) 
            result = MDM.send('AT#SGACT=1,0\r',5)
            res = ftphelp.MDM_waitfor('OK',2) 	  
            result = MDM.send('AT#SGACT=1,1\r', 5)
            res = ftphelp.MDM_waitfor('OK',2)
            kcount = 0
        res = MDM.receive(5)
        print res
        MOD.sleep(5)
        if (res.find('0,1') != -1) or (res.find('1,1') != -1) or (res.find('0,1') != -1) or (res.find('0,5') != -1):
            result = MDM.send('AT#CGPADDR=1\r', 5)
            res = ftphelp.MDM_waitfor('CGPADDR: 1,""',4)
            if res != -1 :
               noIp = 1
               if noIp == 1 :
                   print 'sgact'
                   result = MDM.send('AT#SGACT=1,1\r', 5)
                   res = ftphelp.MDM_waitfor('OK',4)
                   if res != -1 :
                       noIp = 0
                   else :
                       noIp = 1
            else :
              noIp = 0
            if(noIp ==0) :
               print  FTPSERVER_ADDR, FTPUSERNAME, FTPPASSWORD
               a = MDM.send('AT#FTPOPEN="' + FTPSERVER_ADDR + '","' + FTPUSERNAME + '","' + FTPPASSWORD + '",0\r', 5)
               res = ftphelp.MDM_waitfor('OK',50)
               print res
               if (res != -1):
                  print 'FTP Open'
                  ftphelp.Wait(5)
                  a = MDM.send('AT#FTPTYPE=0\r', 0)
                  print a
                  res = ftphelp.MDM_waitfor('OK',20)
                  if(res != -1):
                     print 'Type'
                     ftphelp.Wait(5)
                     a = MDM.send('AT#FTPCWD="'+ DirName +'"\r', 10) 
                     print a
                     resftp = ftphelp.MDM_waitfor('OK',20)
                     if(resftp != -1):
                        print 'Dir'
                        retGetFTP = GetFTPFile(fileName,CheckSum,flag)                  
                        if(retGetFTP == -1):
                           txt = 'GETFTP Err'
                           print txt                           
 
    return 1		   
def savefile(data,filename,CheckSum,flag):
    b = MOD.watchdogReset()
    enddata = data[-25:]
    global datatosave1
    fNoCarrier = enddata.find('NO CARRIER')
    if(fNoCarrier == -1):
        print 'Carrier'
        FileSize = len(data)
    else:
        print 'not carrier'
        lentoCut = 25 - fNoCarrier
        FileSize = len(data)  - lentoCut
    print FileSize
    datatosave = data[:FileSize]
    print datatosave
    checkdata = datatosave[:30]
    res = checkdata.find('CONNECT')
    print res
    if(res != -1):
        print 'CONNECT'
        datatosave = data[res+7:FileSize]
        print datatosave
    datatosave= datatosave.strip()
    print "strip data",datatosave
    if(flag == 1):
       datatosave1 = datatosave
    if(flag ==0):
       md5calc = md5.new(datatosave).digest()
       a = ''
       for x in md5calc:
          a = a + hex(ord(x))
       print a,"MD :",CheckSum
       md5calc = a
       f1 = open("checksum.txt", "a")
       f1.write(md5calc)
       f1.write("Som")
       f1.close()
       if (CheckSum != md5calc):
          print 'md5 error'
#          return -1
    myfile = filename   
    print myfile
    f = open(myfile, "w")
    f.write(datatosave)
    f.close()

    
    return 1
def GetFTPFile(filename,CheckSum,flag):
    b = MOD.watchdogReset()
    strget = 'AT#FTPGET="' + filename + '"\r'
    a = MDM.send(strget, 0 )
    data = ''
    ftphelp.Wait(5)
    timer = MOD.secCounter()
    timeout = MOD.secCounter() + 30 #secondi
    print 'start while'
    while(( MDM.getDCD() != 0) and (timer < timeout)):
        data = data + MDM.read()
        timer = MOD.secCounter()
        if(timer > timeout):
            print 'timeout'
        if(data.find('NO CARRIER') != -1):
            print 'NO CARRIER'
            break
        if(MDM.getDCD() == 0):
            print 'DCD low'
    print data    
    if(len(data) == 0):
        print "No data\r"
        return -1        
    ftphelp.Wait(10)
    print 'Close FTP'
    res = MDM.send('at#ftpclose', 0)
    res = MDM.send('\r', 40)
    res = ftphelp.MDM.receive (10)
    print 'deactivate GPRS'
    MOD.sleep(20)
    MDM.send('+++',20)
    MOD.sleep(20) 			
    result = MDM.send('AT#SH=1\r', 5)
    res = ftphelp.MDM_waitfor('OK',2)      
    result = MDM.send('AT#SGACT=1,0\r', 5)
    res = ftphelp.MDM_waitfor('OK',2)       
    result = MDM.send('AT#SGACT=1,1\r', 5) 
    res = ftphelp.MDM_waitfor('OK',2)
    print 'save file'
    if(flag ==0):
       filename = 'new_'+filename
    saved = savefile(data,filename,CheckSum,flag)
    return saved

def FTP(fileName,CheckSum,flag):
   b = MOD.watchdogReset()
   if(fileName == ''):
      print 'NO FILE'
      okdownl = 0
      return -1
   else:
      print 'ftp'
      okdownl = 1
      if( okdownl == 1):
         res = GetFTP(fileName,CheckSum,flag)
         if(res == -1):
            txt = 'Error FTP'
            print txt
            return -1
      return 1
def mainFTP(FTPSERVER_ADDR1 ,FTPUSERNAME1,FTPPASSWORD1,DirName1,FILENAME):
#      try :
         b = MOD.watchdogReset()
         print 'main ftp'
         global FTPSERVER_ADDR 
         global FTPUSERNAME
         global FTPPASSWORD
         global DirName
         FTPSERVER_ADDR = FTPSERVER_ADDR1
         FTPUSERNAME = FTPUSERNAME1
         FTPPASSWORD = FTPPASSWORD1
         DirName = DirName1
         ret = FTP(FILENAME,0,1)
         if ret != -1:
            print "MD: ",FILENAME
         else :
            return -1
##    here add read file md.txt and keep all filename and its corresponding checksum.
## condsider that each line has file name , checksum.      
         fileList = datatosave1.split(':')
         print "\n",datatosave1
         noOfFile = len(fileList)
         counter = 0
         while counter <  noOfFile :
# here split file name and its checksum.
            filenamehas = fileList[counter].split(',')
            print filenamehas[0]
            print filenamehas[1]
            ret = FTP(filenamehas[0],filenamehas[1],0)
            if ret != -1:
               counter = counter + 1
               print counter
            else :
               return -1
         return 1
#      except Exception, e:
#         print "exep mainFTP"
#         return -1	  