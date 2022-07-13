#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rosbag, cv2
from cv_bridge import CvBridge

bag = rosbag.Bag("/root/data/bag_for_DE.bag", "r")
bag3 = rosbag.Bag("/root/data/assemble_newCRFs.bag", "w")
bridge = CvBridge()

depth_path = "/root/data/newCRFs/"
newimg_path = "/root/data/after/"

t_store = list()
for topic, msg, t in bag.read_messages(topics=["/pylon_camera_node/image_raw", "/rslidar_points"]):
    if topic == "/pylon_camera_node/image_raw":
        new_img = cv2.imread(newimg_path+str(t)+".png", cv2.IMREAD_ANYCOLOR)
        depth_img = cv2.imread(depth_path+str(t)+".png", cv2.IMREAD_ANYDEPTH)
        new_msg = bridge.cv2_to_imgmsg(new_img, "bgr8")
        depth_msg = bridge.cv2_to_imgmsg(depth_img, "mono16")
        bag3.write("/pylon_camera_node/image_raw", new_msg, t)
        bag3.write("/depth_img", depth_msg, t)

    else:
        bag3.write("/rslidar_points", msg, t)
    

bag.close()
bag3.close()
