from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition

def generate_launch_description():

    joy_node = Node(
        package="joy",
        executable="joy_node",
        name="joy_node",
        parameters=[os.path.join(get_package_share_directory("drone_controllers"), "config", "joy_config.yaml")],
        output="screen"
    )
    
    joy_teleop = Node(
        package="joy_teleop",
        executable="joy_teleop",
        name="joy_teleop",
        parameters=[os.path.join(get_package_share_directory("drone_controllers"), "config", "joy_teleop.yaml")],
        output="screen"
    )

    mass_arg = DeclareLaunchArgument(
        name="mass", default_value=0.138
    )

    L_arg = DeclareLaunchArgument(
        name="L", default_value=0.25
    )

    kF_arg = DeclareLaunchArgument(
        name="kF", default_value=3e-5
    )

    kM_arg = DeclareLaunchArgument(
        name="kM", default_value=1.1e-6
    )

    kv_arg = DeclareLaunchArgument(
        name="kv", default_value=24.7
    )

    kp_arg = DeclareLaunchArgument(
        name="kp", default_value=9.35
    )

    kr_arg = DeclareLaunchArgument(
        name="kr", default_value=2.5
    )

    kw_arg = DeclareLaunchArgument(
        name="kw", default_value=0.8
    )
    


    return LaunchDescription([
        joy_node,
        joy_teleop,
    ])