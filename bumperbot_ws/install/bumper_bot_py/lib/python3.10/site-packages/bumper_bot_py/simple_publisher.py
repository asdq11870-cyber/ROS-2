#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__("simple_publisher_node")

        self.pub = self.create_publisher(String, "/publisher", 10)
        self.counter = 0
        self.timer = self.create_timer(0.5, self.publish_msg)

    def publish_msg(self):
        msg = String()
        msg.data = f"Hello {self.counter}"
        self.pub.publish(msg)
        self.get_logger().info(msg.data)
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = SimplePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
