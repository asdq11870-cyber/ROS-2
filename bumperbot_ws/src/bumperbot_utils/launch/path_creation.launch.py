from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
import os

def generate_launch_description():

    trajectory_path = os.path.join(get_package_share_directory("bumperbot_utils"),"launch","trajectory.launch.py")
    controller_launch_path = os.path.join(get_package_share_directory("bumperbot_controller"),"launch","controller.launch.py")
    joystick_launch_path = os.path.join(get_package_share_directory("bumperbot_controller"),"launch","joystick_teleop.launch.py")

    controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(controller_launch_path)
    )

    joystick_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(joystick_launch_path)
            )
        ]
    )

    trajectory_launch = TimerAction(
        period=10.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(trajectory_path)
            )
        ]
    )

    return LaunchDescription([
        controller_launch,
        joystick_launch,
        trajectory_launch
    ])