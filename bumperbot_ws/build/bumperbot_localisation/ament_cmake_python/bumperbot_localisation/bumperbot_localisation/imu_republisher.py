#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
import time

class IMURepublisher(Node):
    def __init__(self):
        super().__init__("imu_republisher_node")

        self.imu_pub = self.create_publisher(Imu,"imu_ekf",10)
        self.imu_sub = self.create_subscription(Imu,"imu/out",self.imuCallback,10)

    def imuCallback(self,imu):
        imu.header.frame_id = "base_footprint_ekf"
        self.imu_pub.publish(imu)

def main(args=None):
    rclpy.init(args=args)
    node = IMURepublisher()
    time.sleep(1)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()