#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <std_msgs/Float32MultiArray.h>

#define PI 3.14159265359

class Roboclaw_Base_Node{
public:
	Roboclaw_Base_Node();

private:
	void encoderCallback(const std_msgs::Float32MultiArray::ConstPtr& encoders);
	
	ros::NodeHandle nh;
	ros::Subscriber enc_sub;
	ros::Publisher odom_pub;
	tf::TransformBroadcaster odom_broadcaster;
	
	double _x, _y, _th;
};

Roboclaw_Base_Node::Roboclaw_Base_Node(){
	_x _y = _th = 0;
	
	// connects subs and pubs
	enc_sub = nh.subscribe<std_msgs::Float32MultiArray>("encoders", 10, &Roboclaw_Base_Node::encoderCallback, this);
	odom_pub = nh.advertise<nav_msgs::Odometry>("odom", 50);
}

void Mecanum_Base_Node::encoderCallback(const std_msgs::Float32MultiArray::ConstPtr& encoders){
	// unpack the encoder message in base_link frame
	ros::Time current_time = ros::Time::now();
	double dx = encoders->data[0];
	double dy = encoders->data[1];
	double dth = encoders->data[2];
	double dt = encoders->data[3];
	
	_x += dx * cos(_th) - dy * sin(_th);
    	_y += dy * cos(_th) + dx * sin(_th);
	
	_th -= dth;
	if (_th > (1.0f * PI)) 
		_th -= (2.0f * PI);
	if (_th < (-1.0f * PI))
		_th += (2.0f * PI);
    
  	// since all odometry is 6DOF we'll need a quaternion created from yaw
	geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(_th);
	
	// first, we'll publish the transform over tf
	geometry_msgs::TransformStamped odom_trans;
	odom_trans.header.stamp = current_time;
	odom_trans.header.frame_id = "odom";
	odom_trans.child_frame_id = "base_link";

	odom_trans.transform.translation.x = _x;
	odom_trans.transform.translation.y = _y;
	odom_trans.transform.translation.z = 0.0;
	odom_trans.transform.rotation = odom_quat;

	// send the transform
	odom_broadcaster.sendTransform(odom_trans);

	// next, we'll publish the odometry message over ROS
	nav_msgs::Odometry odom;
	odom.header.stamp = current_time;
	odom.header.frame_id = "odom";

	// set the position
	odom.pose.pose.position.x = _x;
	odom.pose.pose.position.y = _y;
	odom.pose.pose.position.z = 0.0;
	odom.pose.pose.orientation = odom_quat;

	// set the velocity
	odom.child_frame_id = "base_link";
	odom.twist.twist.linear.x = dx / dt;
	odom.twist.twist.linear.y = dy / dt;
	odom.twist.twist.angular.z = dth / dt;

	// publish the message
	odom_pub.publish(odom);
}

int main(int argc, char** argv){

	ros::init(argc, argv, "roboclaw_base_node");
	Roboclaw_Base_Node Dynamixel_;

	ros::spin();
}
