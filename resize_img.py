#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rosbag, ros_numpy, numpy as np, cv2, pcl
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

TARGET_W, TARGET_H = 1242, 375
RESIZE_W, RESIZE_H = 1326, 706
H_LOWER, H_UPPER = (RESIZE_H - TARGET_H)//2, (RESIZE_H + TARGET_H)//2
W_LOWER, W_UPPER = (RESIZE_W - TARGET_W)//2, (RESIZE_W + TARGET_W)//2

def get_img(src):
    rectification = np.eye(3)

    mapx, mapy = cv2.initUndistortRectifyMap(
        K, D, rectification, K, (W, H), cv2.CV_32FC1)

    calibrated_img = cv2.remap(src, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return calibrated_img

H, W = 1086, 2040
D = np.array([-0.3713184655742523, 0.1894083454473062, 0.0017443421254646307, 0.00037526691609012837, -0.06081438434204424])
K = np.array([[1365.4887468866116, 0.0, 1026.5997744850633],
              [0.0, 1366.2954658193316, 468.9522311262687],
              [0.0, 0.0, 1.0]])

bag = rosbag.Bag("/root/gangnam.bag", "r")
bag2 = rosbag.Bag("/root/gangnam2.bag", "w")
bridge = CvBridge()
for topic, msg, t in bag.read_messages(topics=["/pylon_camera_node/image_raw", "/rslidar_points"]):
    
    if topic == "/pylon_camera_node/image_raw":
        cv_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        img = get_img(cv_img)
        src_resize = cv2.resize(img, (0, 0), fx=0.65, fy=0.65, interpolation=cv2.INTER_AREA)
        im = src_resize[H_LOWER:H_UPPER,W_LOWER:W_UPPER]
        msg = bridge.cv2_to_imgmsg(im, "bgr8")
        bag2.write("/pylon_camera_node/image_raw", msg, t)

    else:
        bag2.write("/rslidar_points", msg, t)
    
    
bag.close()
bag2.close()
