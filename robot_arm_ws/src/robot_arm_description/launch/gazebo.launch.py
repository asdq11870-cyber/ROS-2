from launch import LaunchDescription
from launch_ros.actions import Node
import os
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from pathlib import Path
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():

    robot_arm_description_package = get_package_share_directory("robot_arm_description")
    ros_distro = os.environ["ROS_DISTRO"]
    is_ignition = "True" if ros_distro == "humble" else "False"

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(robot_arm_description_package,"urdf","robot_arm.urdf.xacro")
    )

    world_arg = DeclareLaunchArgument(
        name="world_name",
        default_value="empty"
    )

    world = PathJoinSubstitution([
        robot_arm_description_package, "worlds",
        PythonExpression(expression=["'",LaunchConfiguration("world_name"),"'"," + '.world'"])
    ])

    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("model"), "is_ignition:=",is_ignition]), value_type="str")

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description":robot_description}]
    )

    model_path = str(Path(robot_arm_description_package).parent.resolve())

    return LaunchDescription([

    ])