#!/bin/bash

#Start stage setup
xterm -e roslaunch master stage_mapping.launch &

read -p "Localise robot. Once done, press Enter"

#Run fake_localisation
xterm -e rosrun fake_localization fake_localization & 


#Run cirkit generator to collect waypoints
xterm -e rosrun cirkit_waypoint_generator cirkit_waypoint_generator &

read -p "Drive the robot to desired location. Once done, press Enter"

(cd ~/catkin_ws/src/cirkit_waypoint_manager/cirkit_waypoint_generator && rosrun cirkit_waypoint_generator cirkit_waypoint_saver)

#Save the map
(cd ~/catkin_ws/src/slam_gmapping/gmapping && rosrun map_server map_saver -f dmap)

#Kill the gmapping node
sleep 1
rosnode kill /slam_gmapping

#load map 
xterm -e rosrun map_server map_server dmap.yaml &

#Run AMCL Node
#xterm -e roslaunch amcl amcl.launch &

#Run csv+navigation
(cd ~/catkin_ws/src/cirkit_waypoint_manager/cirkit_waypoint_generator && roslaunch cirkit_waypoint_navigator waypoint_navigator.launch)

