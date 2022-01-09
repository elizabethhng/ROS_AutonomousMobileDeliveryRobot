#!/usr/bin/env python

import csv
import numpy
import os
import rospy


def rotate(qz,qw):
	
	qz_new=abs(qw)
	qw_new=-qz
	
	return qz_new,qw_new
	
path_g=rospy.get_param("/csv_reverse/waypoint_generated_path")
path_o=rospy.get_param("/csv_reverse/waypoint_output_path")

print "path= "+path_g,path_o 

#with open("/cirkit_waypoint_manager/cirkit_waypoint_generator/waypoints_generated.csv","rb") as fr, open("/cirkit_waypoint_manager/cirkit_waypoint_generator/waypoints_output.csv","w") as to:

with open(path_g,"rb") as fr, open(path_o,"w") as to:
	waypoints_in = csv.reader(fr,delimiter=";")
	waypoints_out = csv.writer(to,delimiter=";")
	#cw.writerow(next(cr))  # write title as-is
	data=list(waypoints_in)
	print data
	
	count=0
	for select in data:
		row=select[0].split(',')
	#	print row
		qz= float(row[5])
		qw= float(row[6])
	#	print qz,qw
		
		#qz_new=qz+1
		#qw_new=qw+1
		(qz_new,qw_new)=rotate(qz,qw)
		row[5]=str(qz_new)
		row[6]=str(qw_new)
		s = ', '
		row=s.join(row)
		print row
		
		data[count]=[row]
		count=count+1
		print count
  
	print data
	waypoints_out.writerows(reversed(list(data)))
		
	#reversed(list()
	
  
    #waypoints_out.writerows(reversed(list(waypoints_in)))
