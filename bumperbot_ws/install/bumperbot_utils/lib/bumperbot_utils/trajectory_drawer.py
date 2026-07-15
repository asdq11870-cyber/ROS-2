#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

class TrajectoryDrawer(Node):
    def __init__(self):
        super().__init__("simple_trajectory_drawer")

        self.declare_parameter("odom_topic","bumperbot_controller/odom")
        self.odom_param_ = self.get_parameter("odom_topic").get_parameter_value().string_value
        self.odom_sub_ = self.create_subscription(Odometry,self.odom_param_,self.odomCallback,10)
        self.path_pub_ = self.create_publisher(Path,"bumperbot_controller/trajectory",10)

        self.path_msg = Path()
        self.path_msg.header.frame_id = "odom"


    def odomCallback(self, odom_msg):
        pose_stamped = PoseStamped()
        pose_stamped.header = odom_msg.header
        pose_stamped.pose = odom_msg.pose.pose
        self.path_msg.poses.append(pose_stamped)
        self.path_msg.header.stamp = self.get_clock().now().to_msg()
        self.path_pub_.publish(self.path_msg)


def main(args=None):
    rclpy.init(args=args);
    node = TrajectoryDrawer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()