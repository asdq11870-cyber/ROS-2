#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseNode(Node):
    def __init__(self):
        super().__init__("The_Subscriber_Node")
        self.pose_subscriber = self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)

    def pose_callback(self,msg: Pose):
        self.get_logger().info("(%.2f,%.2f)"%(msg.x,msg.y))

def main(args=None):
    rclpy.init(args=args)
    node = PoseNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()














