cmake_minimum_required(VERSION 3.8)
project(cpp_folder)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rcl_interfaces REQUIRED)
find_package(turtlesim REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(bumperbot_msgs REQUIRED)
find_package(tf2 REQUIRED)

include_directories(include)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_executable(turtle_cpp_publisher src/publisher.cpp)
ament_target_dependencies(turtle_cpp_publisher rclcpp std_msgs geometry_msgs)

add_executable(simple_parameter src/simple_parameter.cpp)
ament_target_dependencies(simple_parameter rclcpp rcl_interfaces)

add_executable(turtlesim_kinematics src/turtlesim_kinematics.cpp)
ament_target_dependencies(turtlesim_kinematics rclcpp turtlesim)

add_executable(simple_tf_kinematics src/simple_tf_kinematics.cpp)
ament_target_dependencies(simple_tf_kinematics rclcpp geometry_msgs tf2_ros)

add_executable(dynamic_tf_kinematics src/dynamic_tf_kinematics.cpp)
ament_target_dependencies(dynamic_tf_kinematics rclcpp geometry_msgs tf2_ros)

add_executable(simple_service_server src/simple_service_server.cpp)
ament_target_dependencies(simple_service_server rclcpp bumperbot_msgs)

add_executable(simple_service_client src/simple_service_client.cpp)
ament_target_dependencies(simple_service_client rclcpp bumperbot_msgs)

add_executable(simple_tf_service src/simple_tf_service.cpp)
ament_target_dependencies(simple_tf_service rclcpp bumperbot_msgs geometry_msgs tf2_ros)

add_executable(euler_to_quaternion src/euler_to_quaternion.cpp)
ament_target_dependencies(euler_to_quaternion rclcpp bumperbot_msgs geometry_msgs tf2_ros tf2)

install(
  DIRECTORY include
  DESTINATION include
)

install(TARGETS 
  turtle_cpp_publisher
  simple_parameter
  turtlesim_kinematics
  simple_tf_kinematics
  dynamic_tf_kinematics
  simple_service_server
  simple_service_client
  simple_tf_service
  euler_to_quaternion
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
