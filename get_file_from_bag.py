#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rosbag, cv2, ros_numpy, numpy as np
from cv_bridge import CvBridge

PATH_img = "/root/data/img/"
PATH_txt = "/root/data/txt/"

bag = rosbag.Bag("/root/data/bag_for_DE.bag", "r")
bridge = CvBridge()

for topic, msg, t in bag.read_messages(topics=["/pylon_camera_node/image_raw"]):
    cv_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imwrite(PATH_img+str(t)+".png", cv_img)


for topic, msg, t in bag.read_messages(topics=["/rslidar_points"]):
    cloud_data = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(msg)
    np.savetxt(PATH_txt+str(t)+".txt", cloud_data)
bag.close()
