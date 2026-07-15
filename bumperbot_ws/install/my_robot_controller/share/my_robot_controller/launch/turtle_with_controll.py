from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_robot_controller',
            executable='wasd_controller',
            name='wasd_controller_node_1',
            output='screen'
        ),
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='sim_node',
            output='screen'

        )
    ])