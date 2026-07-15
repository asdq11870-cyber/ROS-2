from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    gazebo_launch_path = os.path.join(get_package_share_directory("bumper_bot"),"launch","gazebo_localisation.launch.py")
    controller_launch_path = os.path.join(get_package_share_directory("bumperbot_controller"),"launch","controller.launch.py")
    joystick_launch_path = os.path.join(get_package_share_directory("bumperbot_controller"),"launch","joystick_teleop.launch.py")
    local_localisation_path = os.path.join(get_package_share_directory("bumperbot_localisation"),"launch","local_localisation.launch.py")


    use_plotjuggler_arg = DeclareLaunchArgument(
        "use_plotjuggler",
        default_value="True"
    )


    use_plotjuggler = LaunchConfiguration("use_plotjuggler")

    plotjuggler_launcher = TimerAction(
        period=17.0,
        actions=[
            Node(
                package="plotjuggler",
                executable="plotjuggler",
                condition=IfCondition(use_plotjuggler)
            )
            
        ]
    )

    localisation_launcher = TimerAction(
        period=20.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(local_localisation_path)
            )
        ]
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_path)
    )

    controller_launch = TimerAction(
        period=7.5,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(controller_launch_path)
            )
        ]
    )

    joystick_launch = TimerAction(
        period=15.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(joystick_launch_path)
            )
        ]
    )

    return LaunchDescription([
        use_plotjuggler_arg,
        gazebo_launch,
        controller_launch,
        joystick_launch,
        plotjuggler_launcher,
        localisation_launcher
    ])