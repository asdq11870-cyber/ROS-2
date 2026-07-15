#ifndef NOISY_CONTROLLER_HPP
#define NOISY_CONTROLLER_HPP

#include <string>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joint_state.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <memory>
#include <random>
#include <cmath>

class NoisyController : public rclcpp::Node{


public:
    NoisyController(const std::string &name);


private:

    void jointCallback(const sensor_msgs::msg::JointState &msg);

    rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr joint_sub_;
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;

    double wheel_radius_;
    double wheel_separation_;

    double left_wheel_previous_position_;
    double right_wheel_previous_position_;
    rclcpp::Time previous_time_;

    double x_;
    double y_;
    double theta_;

    std::default_random_engine noisy_gen_;
    std::normal_distribution<double> left_encoder_noise_{0.0, 0.005};
    std::normal_distribution<double> right_encoder_noise_{0.0, 0.005};

    nav_msgs::msg::Odometry odom_msg;

    std::unique_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
    geometry_msgs::msg::TransformStamped transform_stamped_;
};

#endif