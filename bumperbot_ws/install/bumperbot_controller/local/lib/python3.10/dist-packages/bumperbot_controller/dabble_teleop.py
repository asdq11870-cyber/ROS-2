#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import json

class DabbleTeleop(Node):
    def __init__(self):
        super().__init__("dabble_teleop")

        # Publish to cmd_vel
        self.pub = self.create_publisher(Twist, "/bumperbot_controller/cmd_vel", 10)

        # UDP setup: port must match Dabble app
        self.udp_ip = "0.0.0.0"  # listen on all interfaces
        self.udp_port = 5555
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.sock.setblocking(False)

        self.timer = self.create_timer(0.05, self.timer_callback)  # 20 Hz

    def timer_callback(self):
        try:
            data, addr = self.sock.recvfrom(1024)
            joystick = json.loads(data.decode("utf-8"))
            twist = Twist()

            # Map joystick axes (example: left stick)
            twist.linear.x = joystick.get("ly", 0.0) * 1.0  # forward/back
            twist.angular.z = joystick.get("lx", 0.0) * 1.0 # turn

            self.pub.publish(twist)

        except BlockingIOError:
            pass  # no data this cycle

def main(args=None):
    rclpy.init(args=args)
    node = DabbleTeleop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
