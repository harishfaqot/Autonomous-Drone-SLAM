#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, PoseWithCovariance, Twist, TwistWithCovariance
import math
import tf

if __name__ == "__main__":
    rospy.init_node("fake_odom_pub")

    pub = rospy.Publisher("/Odometry", Odometry, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    x, y, z = 0.0, 0.0, 0.0
    t = 0.0

    while not rospy.is_shutdown():
        odom = Odometry()
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "map"
        odom.child_frame_id = "base_link"

        # Move in a circle
        x = math.cos(t) * 2.0
        y = math.sin(t) * 2.0
        z = 1.0  # keep altitude at 1m
        t += 0.05

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = z

        quat = tf.transformations.quaternion_from_euler(0, 0, t)
        odom.pose.pose.orientation.x = quat[0]
        odom.pose.pose.orientation.y = quat[1]
        odom.pose.pose.orientation.z = quat[2]
        odom.pose.pose.orientation.w = quat[3]

        odom.twist.twist.linear.x = -math.sin(t) * 2.0
        odom.twist.twist.linear.y = math.cos(t) * 2.0
        odom.twist.twist.linear.z = 0.0

        pub.publish(odom)
        rate.sleep()
