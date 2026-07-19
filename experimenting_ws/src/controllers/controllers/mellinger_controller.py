#!usr/bin/env python3
import rclpy
from rclpy.node import Node

class MellingerController(Node):
    def __init__(self):
        super().__init__("mellinger_controller")

def main(args=None):
    rclpy.init(args=args)
    node = MellingerController()
    rclpy.spin(node=node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()