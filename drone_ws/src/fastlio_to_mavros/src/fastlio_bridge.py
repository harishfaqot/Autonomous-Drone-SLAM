#!/usr/bin/env python3
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, TwistStamped
from mavros_msgs.srv import StreamRate

def odom_cb(msg):
    # Pose
    pose_msg = PoseStamped()
    pose_msg.header = msg.header
    pose_msg.pose = msg.pose.pose
    pub_pose.publish(pose_msg)

def speed_cb(msg):
    # Velocity
    twist_msg = TwistStamped()
    twist_msg.header = msg.header
    twist_msg.twist = msg.twist.twist
    pub_twist.publish(twist_msg)
    print(f"Publish Speed {twist_msg}")

def set_stream_rate(rate_hz=200):
    rospy.wait_for_service("/mavros/set_stream_rate")
    try:
        set_rate_srv = rospy.ServiceProxy("/mavros/set_stream_rate", StreamRate)
        # (stream_id=0 → all, message_rate=rate_hz, on_off=1 → start)
        set_rate_srv(0, rate_hz, 1)
        rospy.loginfo(f"Set MAVROS stream rate to {rate_hz} Hz")
    except rospy.ServiceException as e:
        rospy.logerr(f"Failed to set stream rate: {e}")

if __name__ == "__main__":
    rospy.init_node("fastlio_bridge")

    # Publishers to MAVROS
    pub_pose = rospy.Publisher("/mavros/vision_pose/pose", PoseStamped, queue_size=10)
    pub_twist = rospy.Publisher("/mavros/vision_speed/speed_twist", TwistStamped, queue_size=10)

    # Subscriber to FastLIO odometry (adjust topic if different!)
    rospy.Subscriber("/Odometry", Odometry, odom_cb)
    rospy.Subscriber("/vins_estimator/odometry", Odometry, speed_cb)

    rospy.loginfo("FastLIO → MAVROS bridge started")
    # rospy.spin()
    
    # Loop to enforce stream rate every 1 s
    rate = rospy.Rate(1)  # 1 Hz
    while not rospy.is_shutdown():
        set_stream_rate(200)
        rate.sleep()
