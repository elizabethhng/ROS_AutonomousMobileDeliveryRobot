#!/usr/bin/env python
import serial
import threading
import time
import roslib
import rospy
import struct
from std_msgs.msg import String
from geometry_msgs.msg import Twist


comPort = "/dev/ttyUSB0"

def callback(vel):
    x=format(vel.linear.x,'+.2f')
    z=format(vel.angular.z,'+.2f')
################################################
    pck = x + b',' + z
    rospy.loginfo("Data Transmitting %s",pck)
    # Check the number of bytes to fit the format
    # b'X.XX,X.XX' => 9bytes ;)
    # for separete when received use the "datareceived.split(',')" function 
    if len(pck) == 11:
	comPort.write(pck)
	time.sleep(0.1)


def TransmitThread():
#  while comPort:
      if comPort:        
	rospy.Subscriber("/cmd_vel", Twist, callback )

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

  threading.Thread(target=TransmitThread).start()

  try:
    while True:
      time.sleep(1)
  except:
    comPort = None

if __name__ == "__main__":
  rospy.init_node('com2')
  LoopbackTest(comPort)
  rospy.spin()

