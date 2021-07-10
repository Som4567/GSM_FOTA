# GSM_FOTA
FOTA or OTA ( Firmware over the air using python ) GSM Telit

This python script used to send files using FTP to embedded GSM device to upgrade firmware.

Steps for FOTA or OTA

1. Upload new files ( compiled one) at any server.
2. Send SMS in below format to GSM on mobile number as an interrupt for new firmware availability. 
   **FOTA:ftp.innovations.com:test@innovations.com:Test@1234:telit:FOTA_Test.pyo:OK**   
   
3. GSM will check SMS and connect to corresponding server and make sure all files successfully downloaded using MD5 checksum algorithm.
4. Once New firmware downaloded succesfully then GSM will delete SMS and all other old python files.
5. This whole script is written in python, specially for Telit GL-868 and GL-865 or any GSM module which has inbuilt python interpreter.
