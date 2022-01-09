#!/usr/bin/python
import serial
import threading
import time
import roslib
import rospy
import struct
from std_msgs.msg import String
from geometry_msgs.msg import Twist

comPort = "/dev/ttyUSB0"

def TwistConvertPublish(c):
	(x,z)=c.split(',')
	cmd_vel=Twist()
	cmd_vel.linear.x=float(x)
	cmd_vel.angular.z=float(z)
	pub.publish(cmd_vel)
	

def ReceiveThread():
	while comPort:
		try:
			if comPort.inWaiting() ==11:
				rospy.loginfo("bytes to read %d", comPort.inWaiting())
				c = comPort.read(11)
				TwistConvertPublish(c)
				rospy.sleep(0.1)
		except comPort.inWaiting()==0:
				time.sleep(0.1)
				print ("Sleep")
		except comPort.inWaiting()!=11:
			comPort.flush()
			print("Port Flushed")

		

def LoopbackTest(comPortName):
  global comPort

  comPort = serial.Serial \
            (
              port=comPortName,
              baudrate=115200,
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,
              bytesize=serial.EIGHTBITS
            )

  threading.Thread(target=ReceiveThread).start()

  try:
    while True:
      time.sleep(1)
  except:
    comPort = None

if __name__ == "__main__":
  rospy.init_node('txrx1')
  pub = rospy.Publisher('/cmd_vel', Twist, queue_size=100)
  LoopbackTest(comPort)
  rospy.spin()

