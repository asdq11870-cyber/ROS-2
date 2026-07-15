from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    dabble_teleop = Node(
        package="bumperbot_controller",
        executable="dabble_teleop.py",
        parameters=[os.path.join(get_package_share_directory("bumperbot_controller"),"config","dabble_teleop.yaml")]
    )


    return LaunchDescription([
        dabble_teleop
    ])