#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "Data Transmitting %s", data.data)
    ser.write(data.data)


def listener():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('tx', anonymous=True)

    rospy.Subscriber("/say_hello", String, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

