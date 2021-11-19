import numpy as np
import pysftp
import sys
import time
from subprocess import check_output
scanoutput = check_output(["iwlist", "wlan0", "scan"])

host = "kelp002.local"
password = "pi"
username = "pi"

def wifi_status():
	for line in scanoutput.split():
                line = line.decode("utf-8") 
                if line[:5]  == "ESSID":
                        ssid = line.split('"')[1]
                else:
                        ssid="disconnected"
	return: ssid


while True:
	
	if wifi_status()=="disconnected":
		try:
			ctd_array = []
			for i in range (0,3000):
				conductivity = 32+np.random.random()
				temperature = 45+np.random.random()
				depth = np.random.random()
				ctd_data = round(conductivity,2),round(temperature,2),round(depth,2)
				ctd_array.append(ctd_data)
				if wifi_status()="CellSpot_2.4":
					break
			ctd_array=np.array(ctd_array)
			print(ctd_array)
			dt=0
		except Exception as e:
			print("CTD Measure Error: ",e)
	if wifi_status()=="CellSpot_2.4" and dt==0:
		try:
			np.savetxt('ctd_data.csv',ctd_array,delimiter=',',fmt='%1.3f')
			ctd_array=[]
			print(ctd_array.shape)
			print("CTD saved")
			dt=1
		except Exception as e:
			print("File Save Error: ",e)

		try: 
			time.sleep(300)
			with pysftp.Connection(host, username=username, password=password) as sftp:
				sftp.put("ctd_data.csv","kelp_ctd_manager/src/CTD_Bin/CTD_Data.csv")
		except Exception as e:
			print("Transfer Error: ",e)

