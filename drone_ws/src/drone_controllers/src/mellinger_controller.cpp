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
    Kp = get_parameter("Kp").as_double() * Eigen::Matrix3d::Identity();
    Kv = get_parameter("Kv").as_double() * Eigen::Matrix3d::Identity();
    Kr = get_parameter("Kr").as_double() * Eigen::Matrix3d::Identity();
    Kw = get_parameter("Kw").as_double() * Eigen::Matrix3d::Identity();
    show_logs = get_parameter("show_logs").as_double();

    motor_pub_ = create_publisher<actuator_msgs::msg::Actuators>("/simple_velocity_controller/commands",10);
    ground_truth_sub_ = create_subscription<nav_msgs::msg::Odometry>("/mellinger_controller/odom",10,std::bind(&MellingerControlller::odomCallback,this,_1));
    velocity_sub_ = create_subscription<geometry_msg::msg::TwistStamped>("/mellinger_controller/cmd_vel",10,std::bind(&MellingerController::velCallback,this,_1));
    
    broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(this);
    transform_stamped_.header.frame = "odom";
    transform_stamped.child_frame_id = "root";
    int log_iterator = 0;

    M_ << kF << kF << kF << kF << 0 << -(kF*L) << 0 << (kF*L) << -(kF*L) << 0 << (kF*L) << 0 << -kM << kM << -kM << kM
    inv_M_ = M_.inverse();

    Eigen::Vector3d r_ = Eigen::Vector3d::Zero();
    Eigen::Vector3d vel_ = Eigen::Vector3d::Zero();
    Eigen::Matrix3d R_ = Eigen::Matrix3d::Zero();
    Eigen::Vector3d w_ = Eigen::Vector3d::Zero();

    Eigen::Vector3d r_T_ = Eigen::Vector3d::Zero();
    Eigen::Vector3d vel_T_ = Eigen::Vector3d::Zero();
    double yaw_ = 0.0;
    double yaw_T_ = 0.0;

    auto timer = rclcpp::create_timer(this, this->get_clock(), 0.01, std::bind(&MellingerController::controlLoop, this, _1));
}

void MellingerController::controlLoop(){

}

void MellingerController::velCallback(const geometry_msgs::msg::TwistStamped& msg){
    r_T_ << msg.twist.linear.x << msg.twist.linear.y << msg.twist.linear.z
    vel_T_ << msg.twist.angular.z
}

void MellingerController::odomCallback(const nav_msgs::msg::Odometry& msg){
    r_ << msg.pose.pose.position.x << msg.pose.pose.position.y << msg.pose.pose.position.z
    vel_ << msg.twist.twist.linear.x << msg.twist.twist.linear.y << msg.twist.twist.linear.z
    w_ << msg.twist.twist.angular.x << msg.twist.twist.angular.y << msg.twist.twist.angular.z
    Eigen::Quaterniond q(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,
                        msg.pose.pose.orientation.w);
    R_ = q.toRotationMatrix();

    transform_stamped_.transform.translation.x = r_[0];
    transform_stamped_.transform.translation.y = r_[1];
    transform_stamped_.transform.translation.z = r_[2];
    transform_stamped_.transform.rotation.x = q.x();
    transform_stamped_.transform.rotation.y = q.y();
    transform_stamped_.transform.rotation.z = q.z();
    transform_stamped_.transform.rotation.w = q.w();
    broadcaster_->sendTransform(transform_stamped_);

}

int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MellingerController>("mellinger_controller");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}