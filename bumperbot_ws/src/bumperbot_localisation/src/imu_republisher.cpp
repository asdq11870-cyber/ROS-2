#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/imu.hpp>

using std::placeholders::_1;
using namespace std::chrono_literals;

class IMURepublisher : public rclcpp::Node{

public:
    IMURepublisher() : Node("imu_republisher_node"){
        imu_sub = create_subscription<sensor_msgs::msg::Imu>("/imu/out",10,std::bind(&IMURepublisher::imuCallback,this,_1));
        imu_pub = create_publisher<sensor_msgs::msg::Imu>("/imu_ekf",10);
    }

private:

    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_pub;
    rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub;

    void imuCallback(const sensor_msgs::msg::Imu::SharedPtr imu){
        auto imu_copy = *imu;
        imu_copy.header.frame_id = "base_footprint_ekf";
        imu_pub->publish(imu_copy);
    }
};

int main(int argc, char* argv[]){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<IMURepublisher>();
    rclcpp::sleep_for(1s);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}