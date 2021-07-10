import MDM
import MOD 
import sys
def isfile(filename):
   try :
      f = open(filename, "r")
      f.close();
      return 1
   except Exception, e:
      print 'now log exec'
      return -1



def fileVAL(filename):
    try:
       print "Now will do file validation and replcace old file"
       b = MOD.watchdogReset()
       f = open(filename, "r")
       datatosave=f.read();
       f.close()
       fileList = datatosave.split(':')
       noOfFile = len(fileList)
       counter = 0
       while counter <  noOfFile :
          print fileList[counter]
# here split file name and its checksum.
          filenamehas = fileList[counter].split(',')
          print filenamehas[0]
          filename = 'new_'+filenamehas[0]
          ret =  isfile(filename)
          counter = counter + 1
          if(ret == -1):
             return  -1
          rename(filename,filenamehas[0])
       return 1
    except Exception, e:
       return -1	