#ifndef MELLINGER_CONTROLLER_HPP
#define MELLINGER_CONTROLLER_HPP

#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/twist_stamped.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>

class MellingerController : public rclcpp::Node{
public:
    MellingerController(const std::string& name);
private:
    void odomCallback(const nav_msgs::msg::Odometry& msg);
    void velCallback(const geometry_msgs::msg::TwistStamped& msg);

    rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr motor_pub_;
};


#endif