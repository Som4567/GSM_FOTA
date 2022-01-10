FOTA enables the updation of the software of the integrated M2M modules as and when required.
FOTA makes M2M much more stable and above all more secure.
Any optimizations to the module software can be transferred to the customers applications via the remote software update.

I have created a my own python script to send files to embedded GSM device using FTP to upgrade firmware.

Following are steps for FOTA or OTA

	1.Upload new files ( compiled ones) at any server.
	2.Send SMS in below format to GSM on mobile number as an interrupt for new firmware availability. 
		FOTA:ftp.innovations.com:test@innovations.com:Test@1234:telit:FOTA_Test.pyo:OK
	3.GSM checks SMS and connect to corresponding server. It makes sure that all files have been successfully downloaded successfully by using MD5 checksum algorithm.
	4.Once the new firmware has been downloaded succesfully then GSM will delete SMS and all the other old python files.
	5.This whole script is written in python, specially for Telit GL-868 and GL-865 or any GSM module which has inbuilt python interpreter.
