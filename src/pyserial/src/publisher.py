#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

def talker():
 while not rospy.is_shutdown():
   data= ser.read(1)
   rospy.loginfo(data)
   pub.publish(String(data))
   rospy.sleep(1.0)


if __name__ == '__main__':
  try:
    pub = rospy.Publisher('receiving', String)
    rospy.init_node('rx')
    talker()
  except rospy.ROSInterruptException:
    pass
