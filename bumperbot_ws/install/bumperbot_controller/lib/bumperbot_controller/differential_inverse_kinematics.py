#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray 
from geometry_msgs.msg import TwistStamped, TransformStamped
from sensor_msgs.msg import JointState
import numpy as np
from rclpy.time import Time
from rclpy.constants import S_TO_NS
from nav_msgs.msg import Odometry
from tf_transformations import quaternion_from_euler
from tf2_ros import TransformBroadcaster
import math

class DifferentialInverseController(Node):
    def __init__(self):
        super().__init__("simple_controller")

        self.declare_parameter("wheel_radius",0.033)
        self.declare_parameter("wheel_separation",0.17)

        self.wheel_radius_ = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_separation_ = self.get_parameter("wheel_separation").get_parameter_value().double_value

        self.right_wheel_previous_position_ = 0.0
        self.left_wheel_previous_position_ = 0.0
        self.previous_time_ = self.get_clock().now()

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        self.get_logger().info("Using wheel radius of %.2f"%self.wheel_radius_)
        self.get_logger().info("Using wheel separation of %.2f"%self.wheel_separation_)

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray,"simple_velocity_controller/commands",10)
        self.velocity_sub_ = self.create_subscription(TwistStamped,"bumperbot_controller/cmd_vel",self.velCallback,10)
        self.joint_sub_ = self.create_subscription(JointState,"joint_states", self.jointCallback,10)
        self.odom_pub_ = self.create_publisher(Odometry,"bumperbot_controller/odom",10)

        self.speed_conversion_ = np.array([[self.wheel_radius_/2,self.wheel_radius_/2],[self.wheel_radius_/self.wheel_separation_,-self.wheel_radius_/self.wheel_separation_]])

        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = "odom"
        self.odom_msg.child_frame_id = "base_footprint"
        self.odom_msg.pose.pose.orientation.x = 0.0
        self.odom_msg.pose.pose.orientation.y = 0.0
        self.odom_msg.pose.pose.orientation.z = 0.0
        self.odom_msg.pose.pose.orientation.w = 1.0

        self.broadcaster_ = TransformBroadcaster(self)
        self.transform_stamped_ = TransformStamped()
        self.transform_stamped_.header.frame_id = "odom"
        self.transform_stamped_.child_frame_id = "base_footprint"

        self.inv_speed_conversion_ = np.linalg.inv(self.speed_conversion_)

    def velCallback(self,msg):
        robot_speed = np.array([[msg.twist.linear.x],[msg.twist.angular.z]])

        wheel_speed = np.matmul(self.inv_speed_conversion_,robot_speed)

        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [wheel_speed[0,0],wheel_speed[1,0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def jointCallback(self, msg):
        dp_left = msg.position[1] - self.left_wheel_previous_position_
        dp_right = msg.position[0] - self.right_wheel_previous_position_
        dt = Time.from_msg(msg.header.stamp) - self.previous_time_

        self.left_wheel_previous_position_ = msg.position[1]
        self.right_wheel_previous_position_ = msg.position[0]
        self.previous_time_ = Time.from_msg(msg.header.stamp)

        angular_vel_left = dp_left / (dt.nanoseconds / S_TO_NS)
        angular_vel_right = dp_right / (dt.nanoseconds / S_TO_NS)

        bot_linear = (self.wheel_radius_/2)*(angular_vel_left+angular_vel_right)
        bot_angular = (self.wheel_radius_/self.wheel_separation_)*(angular_vel_right-angular_vel_left)

        d_s = (self.wheel_radius_/2)*(dp_left+dp_right)
        d_theta = (self.wheel_radius_/self.wheel_separation_)*(dp_right-dp_left)
        self.theta_ += d_theta
        self.x_ += (d_s * math.cos(self.theta_))
        self.y_ += (d_s * math.sin(self.theta_))

        q = quaternion_from_euler(0, 0, self.theta_)
        self.odom_msg.pose.pose.orientation.x = q[0]
        self.odom_msg.pose.pose.orientation.y = q[1]
        self.odom_msg.pose.pose.orientation.z = q[2]
        self.odom_msg.pose.pose.orientation.w = q[3]
        self.odom_msg.header.stamp = self.get_clock().now().to_msg()
        self.odom_msg.pose.pose.position.x = self.x_
        self.odom_msg.pose.pose.position.y = self.y_
        self.odom_msg.twist.twist.linear.x = bot_linear
        self.odom_msg.twist.twist.angular.z = bot_angular

        self.transform_stamped_.transform.translation.x = self.x_
        self.transform_stamped_.transform.translation.y = self.y_
        self.transform_stamped_.transform.rotation.x = q[0]
        self.transform_stamped_.transform.rotation.y = q[1]
        self.transform_stamped_.transform.rotation.z = q[2]
        self.transform_stamped_.transform.rotation.w = q[3]
        self.transform_stamped_.header.stamp = self.get_clock().now().to_msg()

        #self.get_logger().info("Linear Velocity: %.2f Angular Velocity: %.2f"%(bot_linear,bot_angular))
        #self.get_logger().info("x: %.2f y: %.2f theta: %.2f"%(self.x_,self.y_,self.theta_))

        self.odom_pub_.publish(self.odom_msg)
        self.broadcaster_.sendTransform(self.transform_stamped_)

def main(args=None):
    rclpy.init(args=args)
    node = DifferentialInverseController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()