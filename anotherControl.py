#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from mavros_msgs.msg import OverrideRCIn
from mavros_msgs.srv import SetMode, CommandBool, CommandTOL

import tf
import math
import time

exec_time = 1/25;

def callback(data):
	pub = rospy.Publisher('/mavros/rc/override', OverrideRCIn, queue_size=10)
    	rate = rospy.Rate(20) # 10hz
	#begin = time.time()
	begin = rospy.Time()
	flag = True
	sign = 1;
	increment = 10;
	pwm2 = 1550;

	while not rospy.is_shutdown():
		list = [1200, pwm2, 1500, 1500, 1000, 1500, 1500, 1500]
		pub.publish(list)
		rospy.loginfo(pwm2)
		rate.sleep()

def setMode():
	print("Set mode")
	rospy.wait_for_service('/mavros/set_mode')
	try:
		modeService = rospy.ServiceProxy('/mavros/set_mode', SetMode)
		modeResponse = modeService(0, 'STABILIZE')
		rospy.loginfo("\nMode Response: " + str(modeResponse))
		print("Mode set")
	except rospy.ServiceException as e:
		print("Service call failed: %s" %e)

def arm():
	print("Set arming")
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
		armResponse = armService(True)
		rospy.loginfo(armResponse)
		print("Armed")
	except rospy.ServiceException as e:
		print("Service call failed: %s" %e)

def disarm():
	print("Set disarming")
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
		armResponse = armService(False)
		rospy.loginfo(armResponse)
		print("Disarmed")
	except rospy.ServiceException as e:
		print("Service call failed: %s" %e)

def control():
	rospy.init_node('control', anonymous=True)
	rospy.Subscriber("/mavros/imu/data", Imu, callback)
	rospy.spin()

if __name__ == '__main__':
	#try:
		print("Program starts")
		setMode()
		arm()
		time.sleep(3)
		control()
	#except rospy.ROSInterrupException:
	#	pass
