#!/usr/bin/env python3
import rclpy
import sys, termios, tty
import threading
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

class TurtleControlNode(Node):
    def __init__(self):
        super().__init__("Turtle_Controller_Node")
        self.cmd_vel = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.pose_subscriber = self.create_subscription(Pose,"/turtle1/pose",self.receive_velocity,10)
        self.get_logger().info("Sending & Receiving Commands!")

    def send_velocity(self):
        msg = Twist()
        while rclpy.ok():
            key = get_key()
            msg.linear.x = 0.0
            msg.angular.z = 0.0
             
            if key == 'w': msg.linear.x = 1.0
            elif key == 'a': msg.angular.z = -1.0
            elif key == 's': msg.linear.x = -1.0
            elif key == 'd': msg.angular.z = 1.0
            elif key == ' ': pass
            elif key == '\x03': rclpy.shutdown()

            

            self.cmd_vel.publish(msg)

    def receive_velocity(self,pose: Pose):
        self.get_logger().info(("%.2f,%.2f")%(pose.x,pose.y))

def main(args=None):
    rclpy.init(args=args)
    node = TurtleControlNode()

    thread = threading.Thread(target=node.send_velocity, daemon=True)
    thread.start()


    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()