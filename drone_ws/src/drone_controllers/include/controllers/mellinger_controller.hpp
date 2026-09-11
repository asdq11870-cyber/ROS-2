#ifndef MELLINGER_CONTROLLER_HPP
#define MELLINGER_CONTROLLER_HPP

#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <actuator_msgs/msg/actuators.hpp>
#include <tf2_ros/transform_broadcaster.hpp>
#include <Eigen/Core>
#include <numpy>

class MellingerController : public rclcpp::Node{
public:
    MellingerController(const std::string& name);
private:
    void odomCallback(const nav_msgs::msg::Odometry& msg);
    void velCallback(const geometry_msgs::msg::TwistStamped& msg);
    void controlLoop();

    rclcpp::Publisher<actuator_msgs::msg::Actuators>::SharedPtr motor_pub_;
    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr ground_truth_sub_;
    rclcpp::Subscription<geometry_msgs::msg::TwistStamped>::SharedPtr velocity_sub_;

    double mass;
    double g;
    double kF;
    double kM;
    Eigen::Matrix3d Kp;
    Eigen::Matrix3d Kv;
    Eigen::Matrix3d Kr;
    Eigen::Matrix3d Kw;
    bool show_logs;

    Eigen::Matrix4d M_;
    Eigen::Matrix4d inv_M_;

    std::unique_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
    geometry_msgs::msg::TransformStamped transform_stamped_;
};

#endif