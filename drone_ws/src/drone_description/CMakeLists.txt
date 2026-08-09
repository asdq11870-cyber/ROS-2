cmake_minimum_required(VERSION 3.8)
project(drone_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rclcpp REQUIRED)
find_package(gz-sim8 REQUIRED)
find_package(yaml-cpp REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
ament_python_install_package(${PROJECT_NAME})


add_library(rotor_thrust_system SHARED
  src/rotor_thrust_system.cpp
)

target_link_libraries(rotor_thrust_system
  gz-sim8::gz-sim8 yaml-cpp
)

target_include_directories(rotor_thrust_system PRIVATE
  /opt/ros/jazzy/opt/gz_sim_vendor/include/gz/sim8
)

install(TARGETS rotor_thrust_system
  LIBRARY DESTINATION lib
)

install(
  DIRECTORY meshes urdf launch rviz worlds
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
