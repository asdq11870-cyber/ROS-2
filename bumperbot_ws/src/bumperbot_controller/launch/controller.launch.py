from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition

def noisy_controller(context, *args, **kwargs):
    wheel_radius_ = float(LaunchConfiguration("wheel_radius").perform(context))
    wheel_separation_ = float(LaunchConfiguration("wheel_separation").perform(context))
    wheel_radius_error_ = float(LaunchConfiguration("wheel_radius_error").perform(context))
    wheel_separation_error_ = float(LaunchConfiguration("wheel_separation_error").perform(context))
    use_python = LaunchConfiguration("use_python")

    noisy_controller_py = Node(
        package="bumperbot_controller",
        executable="noisy_controller.py",
        parameters=[{
            "wheel_radius": wheel_radius_ + wheel_radius_error_,
            "wheel_separation": wheel_separation_ + wheel_separation_error_
        }],
        condition=IfCondition(use_python)
    )

    noisy_controller_cpp = Node(
        package="bumperbot_controller",
        executable="noisy_controller",
        parameters=[{
            "wheel_radius": wheel_radius_ + wheel_radius_error_,
            "wheel_separation": wheel_separation_ + wheel_separation_error_
        }],
        condition=UnlessCondition(use_python)
    )

    return[
        noisy_controller_py,
        noisy_controller_cpp
    ]

def generate_launch_description():

    use_python_arg = DeclareLaunchArgument(
        "use_python",
        default_value="True"
    )

    use_kalman_filter_arg = DeclareLaunchArgument(
        "use_kalman_filter",
        default_value="True"
    )

    wheel_radius_arg = DeclareLaunchArgument(
        "wheel_radius",
        default_value="0.033"
    )
    wheel_separation_arg = DeclareLaunchArgument(
        "wheel_separation",
        default_value="0.17"
    )
    use_diff_inv_arg = DeclareLaunchArgument(
        "use_diff_inv",
        default_value="True"
    )

    use_simple_controller_arg = DeclareLaunchArgument(
        "simple_controller_spawner",
        default_value="False"
    )

    wheel_radius_error_arg = DeclareLaunchArgument(
        "wheel_radius_error",
        default_value="0.005"
    )

    wheel_separation_error_arg = DeclareLaunchArgument(
        "wheel_separation_error",
        default_value="0.02"
    )

    use_wheel_controller_arg = DeclareLaunchArgument(
        "use_wheel_controller", 
        default_value="False"
    )

    use_kalman_filter = LaunchConfiguration("use_kalman_filter")
    use_wheel_controller = LaunchConfiguration("use_wheel_controller")
    use_python = LaunchConfiguration("use_python")
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")
    use_diff_inv = LaunchConfiguration("use_diff_inv")
    use_simple_controller = LaunchConfiguration("simple_controller_spawner")

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster" , "--controller-manager" , "/controller_manager"
        ]
    )

    wheel_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_controller" , "--controller-manager" , "/controller_manager"
        ],
        parameters=[{"topic_name":"/diff_controller/cmd_vel"}],
        condition=IfCondition(use_wheel_controller)
    )

    kalman_filter_launcher = GroupAction(
        condition=IfCondition(use_kalman_filter),
        actions=[
            Node(
                package="bumperbot_localisation",
                executable="kalman_filter.py",
                condition=IfCondition(use_python)
            ),
            Node(
                package="bumperbot_localisation",
                executable="kalman_filter",
                condition=UnlessCondition(use_python)
            )

        ]

    )
    
    differential_inverse_spawner = GroupAction(
        condition=IfCondition(use_diff_inv),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "simple_velocity_controller", "--controller-manager", "/controller_manager"
                ]
            ),
            Node(
                package="bumperbot_controller",
                executable="differential_inverse_kinematics.py",
                parameters=[{"wheel_radius":wheel_radius,"wheel_separation":wheel_separation}],
                condition=IfCondition(use_python)
            ),
            Node(
                package="bumperbot_controller",
                executable="differential_inverse_controller",
                parameters=[{"wheel_radius":wheel_radius,"wheel_separation":wheel_separation}],
                condition=UnlessCondition(use_python)
            )
        ]
    )

    simple_controller = GroupAction(
        condition=IfCondition(use_simple_controller),
        actions=[
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[
                    "simple_velocity_controller" , "--controller-manager" , "/controller_manager"
                ]
            ),

            Node(
                package="bumperbot_controller",
                executable="simple_controller.py",
                parameters=[{"wheel_radius":wheel_radius,"wheel_separation":wheel_separation}],
                condition=IfCondition(use_python)
            ),

            Node(
                package="bumperbot_controller",
                executable="simple_controller",
                parameters=[{"wheel_radius":wheel_radius,"wheel_separation":wheel_separation}],
                condition=UnlessCondition(use_python)
            )
        ]
    )

    noisy_controller_launch = OpaqueFunction(function=noisy_controller)


    return LaunchDescription([
        use_python_arg,
        use_wheel_controller_arg,
        wheel_radius_arg,
        wheel_separation_arg,
        wheel_radius_error_arg,
        wheel_separation_error_arg,
        use_diff_inv_arg,
        use_simple_controller_arg,
        use_kalman_filter_arg,
        joint_state_broadcaster_spawner,
        wheel_controller_spawner,
        differential_inverse_spawner,
        simple_controller,
        noisy_controller_launch,
        kalman_filter_launcher
    ])