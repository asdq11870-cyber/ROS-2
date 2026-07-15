#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class NodeCreation(Node):
    def __init__(self):
        super().__init__("Drawing_Circle_Node")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel",10)
        self.timer = self.create_timer(0.5,self.SendVelocity)
        self.get_logger().info("Drawing a circle!")

    def SendVelocity(self):
        msg = Twist()
        msg.linear.x = 2.0
        #msg.linear.y = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = NodeCreation()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()