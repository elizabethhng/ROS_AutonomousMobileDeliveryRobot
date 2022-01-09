#!/usr/bin/env python
import rospy
import roslaunch
import rospkg
import os
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool

# Initialize variables

buttons_array = [0, 0, 0, 0, 0]
collect_btn_num = 0
collect_btn_sym = ""
send_btn_num = 0
send_btn_sym = ""
calibrate_btn_num = 0
calibrate_btn_sym = ""
abort_btn_num = 0
abort_btn_sym = ""
sim_enabled = False

location_collect = ""
location_send = ""
location_calibrate = ""
location_safety_node = ""

calibrate_complete = False
collect_complete = False
send_complete = False
velocity_paused = False

def getParameter():
    global collect_btn_num
    global collect_btn_sym
    global send_btn_num
    global send_btn_sym
    global calibrate_btn_num
    global calibrate_btn_sym
    global abort_btn_num
    global abort_btn_sym
    global continue_btn_num
    global continue_btn_sym
    global sim_enabled

    collect_btn_num = rospy.get_param("/teleop_twist_joy/collect_button_num")
    collect_btn_sym = rospy.get_param("/teleop_twist_joy/collect_button_sym")
    send_btn_num = rospy.get_param("/teleop_twist_joy/send_button_num")
    send_btn_sym = rospy.get_param("/teleop_twist_joy/send_button_sym")
    calibrate_btn_num = rospy.get_param("/teleop_twist_joy/calibrate_button_num")
    calibrate_btn_sym = rospy.get_param("/teleop_twist_joy/calibrate_button_sym")
    abort_btn_num = rospy.get_param("/teleop_twist_joy/abort_button_num")
    abort_btn_sym = rospy.get_param("/teleop_twist_joy/abort_button_sym")
    continue_btn_num = rospy.get_param("/teleop_twist_joy/continue_button_num")
    continue_btn_sym = rospy.get_param("/teleop_twist_joy/continue_button_sym")
    
    sim_enabled = rospy.get_param("/teleop_twist_joy/sim_enabled")

def getPaths():
    global location_collect
    global location_send
    global location_calibrate
    global location_safety_node
    rospack = rospkg.RosPack()
    
    # Define location of launch files
    if sim_enabled == True:
        location_collect = rospack.get_path('master') + "/launch/stage.launch"
        location_send = rospack.get_path('teleop_twist_joy') + "/launch/include/send_goals_sim.launch"
        location_calibrate = rospack.get_path('teleop_twist_joy') + "/launch/include/heading_calibration_sim.launch"
        location_safety_node = rospack.get_path('teleop_twist_joy') + "/launch/include/safety_node.launch"

    elif sim_enabled == False:
        location_collect = rospack.get_path('teleop_twist_joy') + "/launch/include/collect_goals.launch"
        location_send = rospack.get_path('teleop_twist_joy') + "/launch/include/send_goals.launch"
        location_calibrate = rospack.get_path('teleop_twist_joy') + "/launch/include/heading_calibration.launch"
        location_safety_node = rospack.get_path('teleop_twist_joy') + "/launch/include/safety_node.launch"

    else:
        print("ERROR: PLEASE SPECIFY SIM_ENABLED PARAMETER.")

def joy_CB(joy_msg):
    global start_collect_btn
    global buttons_array 
    buttons_array = [joy_msg.buttons[collect_btn_num],joy_msg.buttons[send_btn_num],joy_msg.buttons[calibrate_btn_num], joy_msg.buttons[abort_btn_num], joy_msg.buttons[continue_btn_num]]

def calibrate_status_CB(calibrate_status_msg):
    global calibrate_complete
    calibrate_complete = calibrate_status_msg.data

def collection_status_CB(collection_status_msg):
    global collect_complete
    collect_complete = collection_status_msg.data

def waypoint_following_status_CB(waypoint_following_status_msg):
    global send_complete
    send_complete = waypoint_following_status_msg.data

def launch_subscribers():
    rospy.init_node('joy_launch_control')
    rospy.Subscriber("/joy_teleop/joy",Joy, joy_CB )
    
def print_instructions():

    print ""
    print "Press %s to start waypoint collection" % collect_btn_sym
    print ""

def check_buttons():

    global buttons_array     
    global launch 
    global calibrate_complete
    global collect_complete
    global send_complete
    global velocity_paused
    

    # Start collecting goals
    if buttons_array[0] == 1:
        while buttons_array[0] == 1:    # Wait for button to be released
            pass
        rospy.loginfo("Starting collect_goals.launch...")
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        launch = roslaunch.parent.ROSLaunchParent(uuid,[location_collect])
        launch.start()


    # Check if end notice has been published by other nodes
    if (calibrate_complete or collect_complete or send_complete):
        rospy.sleep(2) # Sleep for 2 seconds to allow time for other nodes to shutdown
        launch.shutdown()
        print_instructions()
        # Reset all parameters
        calibrate_complete = False
        collect_complete = False
        send_complete = False

def main():

    # start node to subscribe to joy messages node end messages 
    launch_subscribers()

    # check buttons and launch the appropriate file
    while not rospy.is_shutdown():
        check_buttons()
    rospy.spin()

if __name__ == '__main__':

    getParameter()
    getPaths()

    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid,[location_collect])
    print_instructions()

    if sim_enabled == False:
        print("NOTE: It is recommended to perform one or two heading calibrations")
        print("      each time the robot is starting from a new heading.")
    
    main()
    
