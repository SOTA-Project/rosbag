#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rosbag
from cv_bridge import CvBridge

bag = rosbag.Bag("/root/gangnam2.bag", "r")
bag3 = rosbag.Bag("/root/data/bag_for_DE.bag", "w")
bridge = CvBridge()

cnt = 0
time_store = 0
for topic, msg, t in bag.read_messages(topics=["/pylon_camera_node/image_raw", "/rslidar_points"]):
    if topic == "/pylon_camera_node/image_raw":
        if cnt ==1:
            bag3.write("/pylon_camera_node/image_raw", msg, time_store)
            cnt = 0

    else:
        bag3.write("/rslidar_points", msg, t)
        time_store = t
        cnt = 1
    
    
bag.close()
bag3.close()
