#!/usr/bin/env python3
from functools import partial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

class AutoNode(Node):
    def __init__(self):
        super().__init__("Automatic_Robot")
        self.cmd_vel = self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.pose_subscriber = self.create_subscription(Pose,"/turtle1/pose",self.receive_velocity,10)
        self.timer = self.create_timer(0.5,self.send_velocity)
        self.pose = None
        self.get_logger().info("Sending & Receiving Commands!")

    def send_velocity(self):

        if self.pose is None:
            return
        msg = Twist()
        if self.pose.x > 9 or self.pose.x < 2 or self.pose.y > 9 or self.pose.y < 2:
            msg.linear.x = 1.0
            msg.angular.z = 0.9
        else:
            msg.linear.x = 5.0
            msg.angular.z = 0.0
        self.cmd_vel.publish(msg)

        if self.pose.x > 5.5 and self.pose.y > 5.5:
            self.call_set_pen_service(255,0,0,3,0)
        elif self.pose.x < 5.5 and self.pose.y > 5.5:
            self.call_set_pen_service(0,255,0,3,0)
        elif self.pose.x > 5.5 and self.pose.y < 5.5:
            self.call_set_pen_service(0,0,255,3,0)
        else:
            self.call_set_pen_service(45,28,99,3,0)

    def call_set_pen_service(self, r, g, b, width, off):
        client = self.create_client(SetPen, "/turtle1/set_pen")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for service...")
        
        request = SetPen.Request()
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off

        future = client.call_async(request)
        future.add_done_callback(partial(self.callback_set_pen))

    def callback_set_pen(self, future):
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().error("Service failed!")
        
    def receive_velocity(self,pose:Pose):
        self.pose = pose
        self.get_logger().info(("%.2f,%.2f")%(pose.x,pose.y))


def main(args=None):
    rclpy.init(args=args)
    node = AutoNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()