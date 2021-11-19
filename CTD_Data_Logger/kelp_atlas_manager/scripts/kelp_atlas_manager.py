#!/usr/bin/python3
# license removed for brevity

import rospy
from std_msgs.msg import Float64
import atlas_functions as k
import math
import time
def tempcondtosal(incond,intemp):
        incond=float(incond)
        intemp=float(intemp)
        ok=0
        a0=0.008
        a1=-0.1692
        a2=25.3851
        a3=14.0941
        a4=-7.0261
        a5=2.7081
        b0=0.0005
        b1=-0.0056
        b2=-0.0066
        b3=-0.0375
        b4=0.0636
        b5=-0.0144
        c0=0.6766097
        c1=0.0200564
        c2=0.0001104259
        c3=-0.00000069698
        c4=0.0000000010031
         
        r=incond/ 42914.0
        r =r / (c0+intemp*(c1+intemp*(c2+intemp*(c3+intemp*c4))))
        r2=math.sqrt(r)
        ds=b0+r2*(b1+r2*(b2+r2*(b3+r2*(b4+r2*b5))))
        ds=ds*((intemp-15.0)/(1.0+0.0162*(intemp-15.0)))
        sal=a0+r2*(a1+r2*(a2+r2*(a3+r2*(a4+r2*a5))))+ds
        return sal





def atlas_manager():
	pub_do2 = rospy.Publisher('do2', Float64, queue_size=10)
	pub_sal = rospy.Publisher('salinity', Float64, queue_size=10)
	pub_cond = rospy.Publisher('conductivity', Float64, queue_size=10)
	pub_temp = rospy.Publisher('water_temperature', Float64, queue_size=10)
	pub_ph = rospy.Publisher('ph', Float64, queue_size=10)
	rospy.init_node('kelp_atlas_manager', anonymous=True)
	rate = rospy.Rate(0.01666) #
	while not rospy.is_shutdown():

        #external_ = round(sense.get_corrected_temperature(),2)
        #external_humidity = round(sense.get_humidity(),2)
		try:
			
			do2=k.measure(k.DO_Ping())
			water_temp=k.measure(k.RTD_Ping())
			cond=k.measure(k.EC_Ping())
			ph=k.measure(k.pH_Ping())
			sal=tempcondtosal(cond,water_temp)
			
			#####BROKEN CODE

			#cond=10000000
			#do2=10000000
			#water_temp=10000000
			#ph=10000000
			#sal=10000000

			#cond="c"
			#do2="a"
			#water_temp="b"
			#ph="d"
			#sal="e"

	
			print('do2 ',do2)
			print('T ',water_temp)
			print('Cond ',cond)
			print('pH ',ph)
			print('Sal ',sal)
			rospy.loginfo("publishing")
		except Exception as e:
			print(e)
			pass
		try:
			pub_do2.publish(do2)
		except Exception as e:
			print(e)
			pass

		try:
			pub_sal.publish(sal)
		except Exception as e:
			print(e)
			pass
	
		try:
			pub_cond.publish(cond)
		except Exception as e:
			print(e)
			pass
		try:
			pub_temp.publish(water_temp)
		except Exception as e:
			print(e)
			pass
		try:
			pub_ph.publish(ph)

		except Exception as e:
			print(e)
			continue
		rate.sleep()
if __name__ == '__main__':
    try:
        atlas_manager()
    except rospy.ROSInterruptException:
        pass
