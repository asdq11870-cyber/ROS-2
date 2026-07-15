#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"

using namespace std::chrono_literals;

int main(int argc, char* argv[]){
    rclcpp::init(argc,argv);
    auto node = rclcpp::Node::make_shared("Turtle_controller");
    auto pub=
        node->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
    rclcpp::Rate loop_rate(10);
    while(rclcpp::ok()){
        geometry_msgs::msg::Twist msg;
        msg.linear.x = 2.0;
        msg.angular.z = 1.0;
        pub -> publish(msg);
        rclcpp::spin_some(node);
        loop_rate.sleep();
    }
    rclcpp::shutdown();
}