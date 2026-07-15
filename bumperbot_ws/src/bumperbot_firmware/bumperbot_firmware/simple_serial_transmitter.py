#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

class SimpleSerialTransmitter(Node):
    def __init__(self):
        super().__init__("simple_serial_transmitter")
        self.declare_parameter("port")
        self.arduino = serial.Serial()
        self.sub = self.create_subscription(String, "serial_transmitter",self.msgCallback, 10)
        self.sub
        
    def msgCallback(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = SimpleSerialTransmitter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()