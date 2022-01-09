#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from numpy import inf


def callback(msg):
    a=min(msg.ranges[1:22])
    b=min(msg.ranges[23:44])
    c=min(msg.ranges[41:66])
    d=min(msg.ranges[67:88])
    e=min(msg.ranges[89:110])  
    f=min(msg.ranges[111:132])
    print(a,b,c,d,e,f)
    
    a=colourassign(a)
    b=colourassign(b)
    c=colourassign(c)
    d=colourassign(d)
    e=colourassign(e)
    f=colourassign(f)

    
    print(a,b,c,d,e,f)
    
def	colourassign(x):

		if (x>0 and x<=1):
			color="r"
			
		elif (x>1 and x<=2):
			color="y"
			
		elif (x>2):
			color="g"
			
		elif (x==inf):
			color="g"
			
		else:
			color="x"
	
		return color
			
			
def length(x):
		print len(x.ranges)

rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
#sub = rospy.Subscriber('/scan', LaserScan, length)
rospy.spin()
