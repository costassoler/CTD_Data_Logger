import numpy as np
import tsys01 #thermometer library
from kellerLD import KellerLD #pressure sensor library
import atlas_functions as k #conductivity sensor library
import pysftp
import sys
import time
host = "kelp002.local"
password = "pi"
username = "pi"

cond = k.measure(k.EC_Ping())

sensorT = tsys01.TSYS01()
sensorT.init()
sensorT.read()

sensorD = KellerLD()
sensorD.init()
sensorD.read()
while True:
	try:
		ctd_array = []
		print("Recording")
		for i in range (0,300):
			conductivity = k.measure(k.EC_Ping())
			sensorT.read()
			temperature = sensorT.temperature()
			sensorD.read()
			depth=sensorD.pressure()
			ctd_data = round(conductivity,2),round(temperature,2),round(depth,2)
			ctd_array.append(ctd_data)
			print(ctd_data)
		ctd_array=np.array(ctd_array)
		print(ctd_array)
	except Exception as e:
		print("CTD Measure Error: ",e)

	try:
		np.savetxt('ctd_data.csv',ctd_array,delimiter=',',fmt='%1.3f')
		print(ctd_array.shape)
		print("CTD saved")
		
	except Exception as e:
		print("File Save Error: ",e)

	try: 
		time.sleep(300)
		with pysftp.Connection(host, username=username, password=password) as sftp:
			sftp.put("ctd_data.csv","kelp_ctd_manager/src/CTD_Bin/CTD_Data.csv")
	except Exception as e:
		print("Transfer Error: ",e)

