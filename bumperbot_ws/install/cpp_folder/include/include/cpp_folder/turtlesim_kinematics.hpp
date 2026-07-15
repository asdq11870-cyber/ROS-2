#ifndef TURTLESIM_KINEMATICS_HPP
#define TURTLESIM_KINEMATICS_HPP

#include <rclcpp/rclcpp.hpp>
#include <turtlesim/msg/pose.hpp>

class SimpleTurtleKinematics : public rclcpp::Node{
public:
    SimpleTurtleKinematics(const std::string &name);

private:
    void turtle1PoseCallbacks(const turtlesim::msg::Pose &position);

    void turtle2PoseCallbacks(const turtlesim::msg::Pose &position);

    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr turtle1_pose_sub_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr turtle2_pose_sub_;

    turtlesim::msg::Pose last_turtle1_pose_;
    turtlesim::msg::Pose last_turtle2_pose_;

};

#endif