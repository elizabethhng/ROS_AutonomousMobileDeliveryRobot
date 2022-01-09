import rospy
from geometry_msgs.msg import Twist

rospy.init_node('....', anonymous=True)
velocity_publisher=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
vel_msg=Twist()

vel_msg.linear.x=speed_linear
vel_msg.linear.y=0
vel_msg.linear.z=0
vel_msg.angular.x=0
vel_msg.angular.x=0
vel_msg.angular.z=speed_angular


velocity_publisher.publish(vel_msg)
