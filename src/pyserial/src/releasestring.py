#! /usr/bin/env python

import rospy
from std_msgs.msg import String

rospy.init_node('com_2')

publisher = rospy.Publisher('/say_hello', String, queue_size=1)
rate = rospy.Rate(0.1) # 3 Hz

while not rospy.is_shutdown():
    publisher.publish('Hi')
    rate.sleep()
