#include "mellinger_controller.hpp"
#include <Eigen/Geometry>
using std::placeholders::_1;

MellingerController::MellingerController(const std::string& name) : Node(name){
    declare_parameter("mass",0.138);
    declare_parameter("g",9.81);
    declare_parameter("L",0.12);
    declare_parameter("kF",3.0e-5);
    declare_parameter("kM",1.1e-6);
    declare_parameter("Kp",2.0);
    declare_parameter("Kv",1.0);
    declare_parameter("Kr",0.1);
    declare_parameter("Kw",0.05);
    declare_parameter("show_logs",false);

    mass = get_parameter("mass").as_double();
    g = get_parameter("g").as_double();
    L = get_parameter("L").as_double();
    kF = get_parameter("kF").as_double();
    kM = get_parameter("kM").as_double();
    Kp = get_parameter("Kp").as_double();
    Kv = get_parameter("Kv").as_double();
    Kr = get_parameter("Kr").as_double();
    Kw = get_parameter("Kw").as_double();
    show_logs = get_parameter("show_logs").as_double();

    motor_pub_ = create_publisher<actuator_msgs::msg::Actuators>("/simple_velocity_controller/commands",10);
    ground_truth_sub_ = create_subscription<nav_msgs::msg::Odometry>("/mellinger_controller/odom",10,std::bind(&MellingerControlller::odomCallback,this,_1));
    velocity_sub_ = create_subscription<geometry_msg::msg::TwistStamped>("/mellinger_controller/cmd_vel",10,std::bind(&MellingerController::velCallback,this,_1));
    
}

MellingerController::controlLoop(){

}

MellingerController::velCallback(const geometry_msgs::msg::TwistStamped& msg){

}

MellingerController::odomCallback(const nav_msgs::msg::Odometry){
    
}

int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MellingerController>("mellinger_controller");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}