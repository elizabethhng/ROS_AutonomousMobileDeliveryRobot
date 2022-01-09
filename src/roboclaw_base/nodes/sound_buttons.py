#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from sound_play.msg import SoundRequest

PS3_BUTTON_ACTION_TRIANGLE = 12
PS3_BUTTON_ACTION_CIRCLE = 13
PS3_BUTTON_ACTION_CROSS = 14
PS3_BUTTON_ACTION_SQUARE = 15
PS3_BUTTON_PAIRING = 16

class Sound_Request():
    def __init__(self):
        rospy.init_node('sound_buttons', anonymous=False)
   	
	#what to do if shut down (e.g. ctrl + C or failure)
	rospy.on_shutdown(self.shutdown)
	 
    #def callback(data):
    	#print(data.buttons[2])

    #def main():

	while not rospy.is_shutdown():

    	    self.pub = rospy.Publisher('/robotsound', SoundRequest, queue_size=10)

    	#rospy.init_node('sound_buttons', anonymous=True)
    	    self.rate = rospy.Rate(10)
	    #directory of file with sounds
	    self.soundDir = '/home/robo/Music/'

    	#rospy.Subscriber("joy", Joy, callback)
    	#if (data.button[12]==PS3_BUTTON_ACTION_TRIANGLE)
    	    sound = self.sendMsg(filename = 'Drinks.wav')      
    	    self.rate.sleep()

    def sendMsg(self,filename):
    	self.msg = SoundRequest()
    	self.msg.sound = -2
    	self.msg.command = 1
    	self.msg.arg = self.soundDir + filename
    	self.msg.arg2 = ''
    	self.pub.publish(self.msg)

    def shutdown(self):
        rospy.loginfo("Shutting down node...")         
    
if __name__ == '__main__':
    try:
	Sound_Request()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
