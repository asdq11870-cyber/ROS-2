#include "cpp_folder/simple_tf_kinematics.hpp"

SimpleTFKinematics::SimpleTFKinematics(const std::string &name) : Node(name){
    static_tf_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    static_transform_stamped_.header.stamp = get_clock()->now();
    static_transform_stamped_.header.frame_id = "bumperbot_base";
    static_transform_stamped_.child_frame_id = "bumperbot_top";
    static_transform_stamped_.transform.translation.x = 0.0;
    static_transform_stamped_.transform.translation.y = 0.0;
    static_transform_stamped_.transform.translation.z = 0.3;
    static_transform_stamped_.transform.rotation.x = 0.0;
    static_transform_stamped_.transform.rotation.y = 0.0;
    static_transform_stamped_.transform.rotation.z = 0.0;
    static_transform_stamped_.transform.rotation.w = 1.0;

    static_tf_broadcaster_->sendTransform(static_transform_stamped_);

    std::string header = static_transform_stamped_.header.frame_id;
    std::string child = static_transform_stamped_.child_frame_id;

    RCLCPP_INFO_STREAM(get_logger(),"Publishing static transformation between " << header << " and " << child);

}

int main(int argc, char* argv[]){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<SimpleTFKinematics>("simple_tf_kinematics");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}