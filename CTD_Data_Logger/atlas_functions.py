import io
import re
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	AtlasI2C
)
def get_devices():
	device = AtlasI2C()
	device_address_list = device.list_i2c_devices()
	device_list = []

	for i in device_address_list:
		try:
			device.set_i2c_address(i)
			response = device.query("I")
			moduletype = response.split(",")[1]
			response = device.query("name,?").split(",")[1]
			device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
		except Exception as e:
			#print(e)
			continue
	return device_list

def DO_Ping():
	'''Returns the string readout from DO sensor'''	
	DO_Read="DO:999.0"
	device_list = get_devices()
	device = device_list[0]
	
	for dev in device_list:
		dev.write("R")
	time.sleep(1)
	for dev in device_list:
		try:
			a=dev.read()
			if ("DO" in a):
				DO_Read=a.replace('\x00','')
				DO_Read.replace('\x01','')
				DO_Read.replace('\x02','')
				DO_Read.replace('\x03','')
				DO_Read.replace('\x04','')
				DO_Read.replace('\x05','')
				DO_Read.replace('\x06','')
				DO_Read.replace('\x07','')
				DO_Read.replace('\x08','')
				DO_Read.replace('\x09','')
		except Exception as e:
			print(e)
			continue
	return DO_Read

def RTD_Ping():
	'''Returns the string readout from Temperature Sensor'''
	RTD_Read="RTD:999.0"
	device_list = get_devices()

	for dev in device_list:
		dev.write("R")
	time.sleep(1)
	for dev in device_list:
		try:
			a=dev.read()
			if("RTD" in a):
				RTD_Read = a.replace('\x00','')
				RTD_Read.replace('\x01','')
				RTD_Read.replace('\x02','')
				RTD_Read.replace('\x03','')
				RTD_Read.replace('\x04','')
				RTD_Read.replace('\x05','')
				RTD_Read.replace('\x06','')
				RTD_Read.replace('\x07','')
				RTD_Read.replace('\x08','')
				RTD_Read.replace('\x09','')
		except Exception as e:
			print(e)
			continue

	return RTD_Read


def pH_Ping():
	pH_Read="PH:999.0"
	'''Returns the string readout from DO sensor''' 
	device_list = get_devices()
	device = device_list[0]

	for dev in device_list:
		dev.write("R")
	time.sleep(1)
	for dev in device_list:
		try:
			a=dev.read()
			a.encode('ascii',errors='ignore')
			if ("pH" in a):
				pH_Read=a.replace('\x00','')
				pH_Read.replace('\x01','')
				pH_Read.replace('\x02','')
				pH_Read.replace('\x03','')
				pH_Read.replace('\x04','')
				pH_Read.replace('\x05','')
				pH_Read.replace('\x06','')
				pH_Read.replace('\x07','')
				pH_Read.replace('\x08','')
				pH_Read.replace('\x09','')
		except Exception as e:
			print(e)
			continue

	return pH_Read

def EC_Ping():
	EC_Read="EC:999.0"
	'''Returns the string readout from Conductivity sensor'''
	device_list = get_devices()
	device = device_list[0]
        
	for dev in device_list:
		dev.write("R")
	time.sleep(1)
	for dev in device_list:
		try:
			a=dev.read()
			a.encode('ascii',errors='ignore')
			if ("EC" in a):
				EC_Read=a.replace('\x00','')
				EC_Read.replace('\x01','')
				EC_Read.replace('\x02','')
				EC_Read.replace('\x03','')
				EC_Read.replace('\x04','')
				EC_Read.replace('\x05','')
				EC_Read.replace('\x06','')
				EC_Read.replace('\x07','')
				EC_Read.replace('\x08','')
				EC_Read.replace('\x09','')
		except Exception as e:
			print(e)
			continue
	return EC_Read

def measure(i2cString):
	n=0
	while True:
		n+=1
		try:
			rec = i2cString.split(":")
			deviceInfo=rec[0]
			reading=rec[1]
			floatMeas=float(reading)
			break
		except:
			if(n>=10):
				floatMeas=999.0
				break
			i2cString
			
			continue

	return floatMeas

def ping():
	device_list = get_devices()
	device = device_list[0]
	EC_Read="NA"
	DO_Read="NA"
	RTD_Read="NA"
	pH_Read="NA" 
	while True:
		for dev in device_list:
			dev.write("R")
		time.sleep(1)
		for dev in device_list:
			a=dev.read().replace('\x00','')
			if ("EC" in a):
				EC_Read=a
			if("DO" in a):
				DO_Read=a
			if("RTD" in a):
				RTD_Read=a
			if("pH" in a):
				pH_Read=a
			print(EC_Read,DO_Read,RTD_Read,pH_Read)


def avgMeas():
	device_list = get_devices()
	device = device_list[0]
	while True:
					
		for dev in device_list:
			dev.write("R")
		time.sleep(1)
		for dev in device_list:
			readings = dev.read().split(":")
			deviceNum = readings[0]
			meas=re.findall(r"[-+]?\d*\.\d+|\d+", readings[1])
			condMeas=float(meas[0])
			print(condMeas)

def avgMeas30sec():
	device_list = get_devices()
	device      = device_list[0]
	condMeasSum=0
	samples=30
	for i in range (0,samples):
		for dev in device_list:
			dev.write("R")
		time.sleep(1)
		for dev in device_list:
			readings = dev.read().split(":")
			deviceNum = readings[0]
			meas=re.findall(r"[-+]?\d*\.\d+|\d+", readings[1])
			condMeas=float(meas[0])
		condMeasSum+=condMeas
	averageCondMeas=condMeasSum/samples
	print(averageCondMeas)
	return averageCondMeas
'''
while True:
	avgMeas30sec()
	time.sleep(900)
'''
