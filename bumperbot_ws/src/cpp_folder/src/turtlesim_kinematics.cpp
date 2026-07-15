#include "cpp_folder/turtlesim_kinematics.hpp"
#include <cmath>

using std::placeholders::_1;

SimpleTurtleKinematics::SimpleTurtleKinematics(const std::string &name) : Node(name){
    turtle1_pose_sub_ = create_subscription<turtlesim::msg::Pose>("/turtle1/pose",10,
        std::bind(&SimpleTurtleKinematics::turtle1PoseCallbacks,this,_1));
    turtle2_pose_sub_ = create_subscription<turtlesim::msg::Pose>("/turtle2/pose",10,
        std::bind(&SimpleTurtleKinematics::turtle2PoseCallbacks,this,_1));
}


void SimpleTurtleKinematics::turtle1PoseCallbacks(const turtlesim::msg::Pose &position){
    last_turtle1_pose_ = position;
}

void SimpleTurtleKinematics::turtle2PoseCallbacks(const turtlesim::msg::Pose &position){
    last_turtle2_pose_ = position;

    double Tx = last_turtle2_pose_.x - last_turtle1_pose_.x;
    double Ty = last_turtle2_pose_.y - last_turtle1_pose_.y;

    double theta = last_turtle2_pose_.theta - last_turtle1_pose_.theta;
    double theta_deg = theta * (180.0/M_PI);

    double sine = std::sin(theta);
    double cosine = std::cos(theta);


    RCLCPP_INFO_STREAM(get_logger(), "\nTranslation & Rotation Vector & Matrix t1 to t2\n" <<
            "Tx: " << Tx << "\n" <<
            "Ty: " << Ty << "\n" << 
            "Theta(rad): " << theta << "\n" <<
            "Theta(deg): " << theta_deg << "\n" <<
            "| " << cosine << " " << -sine << " |" << "\n" <<
            "| " << cosine << " " << sine << " |" << "\n");
}


int main(int argc, char* argv[]){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<SimpleTurtleKinematics>("Simple_turtle_kinematics");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}