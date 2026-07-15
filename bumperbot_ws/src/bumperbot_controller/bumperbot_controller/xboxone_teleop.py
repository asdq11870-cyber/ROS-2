#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from evdev import InputDevice, ecodes, list_devices
import threading

class XBOXTeleop(Node):
    def __init__(self):
        super().__init__('xbox_teleop')
        self.pub = self.create_publisher(Joy, '/joy', 10)

        devices = [InputDevice(fn) for fn in list_devices()]
        self.dev = None

        for d in devices:
            if 'Xbox Wireless Controller' in d.name \
            and 'Keyboard' not in d.name \
            and 'Consumer' not in d.name:
                self.dev = InputDevice(d.path)
                break

        if not self.dev:
            self.get_logger().error("Xbox controller NOT found")
            return

        self.get_logger().info(f'Using device: {self.dev.name}')

        self.msg = Joy()
        self.msg.axes = [0.0]*8
        self.msg.buttons = [0]*15

        threading.Thread(target=self.read_loop, daemon=True).start()

    def read_loop(self):
        for event in self.dev.read_loop():

            if event.type == ecodes.EV_ABS:
                if event.code == ecodes.ABS_X:
                    self.msg.axes[0] = event.value/32767.0
                elif event.code == ecodes.ABS_Y:
                    self.msg.axes[1] = event.value/32767.0
                elif event.code == ecodes.ABS_RX:
                    self.msg.axes[3] = event.value/32767.0

            elif event.type == ecodes.EV_KEY:
                if 304 <= event.code <= 317:
                    self.msg.buttons[event.code-304] = event.value

            self.msg.header.stamp = self.get_clock().now().to_msg()
            self.pub.publish(self.msg)

def main():
    rclpy.init()
    node = XBOXTeleop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

