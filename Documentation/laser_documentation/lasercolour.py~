#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from numpy import inf


def callback(msg):
    a=min(msg.ranges[1:22])
    a=colourassign(a)
    b=min(msg.ranges[23:44])
    b=colourassign(b)
    c=min(msg.ranges[41:66])
    c=colourassign(c)
    d=min(msg.ranges[67:88])
    d=colourassign(d)
    e=min(msg.ranges[89:110])
    e=colourassign(e)
    f=min(msg.ranges[111:132])
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
	
		print (color+"looped")
		
		return color
			
			
			
def length(x):
		print len(x.ranges)

rospy.init_node('scan_values')
sub = rospy.Subscriber('/scan', LaserScan, callback)
#sub = rospy.Subscriber('/scan', LaserScan, length)
rospy.spin()
