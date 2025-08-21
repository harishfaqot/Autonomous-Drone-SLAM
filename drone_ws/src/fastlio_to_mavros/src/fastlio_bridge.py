#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, TwistStamped

def odom_cb(msg):
    # Pose
    pose_msg = PoseStamped()
    pose_msg.header = msg.header
    pose_msg.pose = msg.pose.pose
    pub_pose.publish(pose_msg)

    # Velocity
    twist_msg = TwistStamped()
    twist_msg.header = msg.header
    twist_msg.twist = msg.twist.twist
    pub_twist.publish(twist_msg)

if __name__ == "__main__":
    rospy.init_node("fastlio_bridge")

    # Publishers to MAVROS
    pub_pose = rospy.Publisher("/mavros/vision_pose/pose", PoseStamped, queue_size=10)
    pub_twist = rospy.Publisher("/mavros/vision_speed/speed_twist", TwistStamped, queue_size=10)

    # Subscriber to FastLIO odometry (adjust topic if different!)
    rospy.Subscriber("/Odometry", Odometry, odom_cb)

    rospy.loginfo("FastLIO → MAVROS bridge started")
    rospy.spin()
