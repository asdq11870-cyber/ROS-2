from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d",os.path.join(get_package_share_directory("bumper_bot"),"rviz","display2.rviz")]
    )

    trajectory_node = Node(
        package="bumperbot_utils",
        executable="trajectory_drawer.py",
        output="screen",
        parameters=[{"odom_topic":"bumperbot_controller/odom"}]
    )



    return LaunchDescription([
        rviz_node,
        trajectory_node,
    ])

