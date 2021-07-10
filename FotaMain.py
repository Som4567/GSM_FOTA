import MOD
MOD.watchdogDisable()
import setup
import sms
	
b = MOD.watchdogReset()
def Main():
   try :
     ret = sms.main_sms()
     if ret == 1 :
        import ftp 
        retFTP = ftp.mainFTP(sms.FTPSERVER_ADDR ,sms.FTPUSERNAME,sms.FTPPASSWORD,sms.DirName,sms.FILENAME)
        if(retFTP == 1):
           import VALIDATE
           retVAL = VALIDATE.fileVAL(sms.FILENAME)
           if(retVAL == 1):
              sms.delsms()
              MOD.watchdogDisable()
              MOD.watchdogEnable(1)
              while 1:
                 print 'IN restrt'
   finally:
     import Main



#sms.delsms()
Main()

