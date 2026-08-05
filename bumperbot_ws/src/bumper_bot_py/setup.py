from setuptools import find_packages, setup

package_name = 'bumper_bot_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='unknown',
    maintainer_email='unknown@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "simple_parameter = bumper_bot_py.parameter_simple:main",
            "turtlesim_kinematics = bumper_bot_py.turtlesim_kinematics:main",
            "turtlesim_rotation = bumper_bot_py.turtlesim_rotation:main",
            "simple_tf_kinematics = bumper_bot_py.simple_tf_kinematics:main",
            "dynamic_tf_kinematics = bumper_bot_py.dynamic_tf_kinematics:main",
            "simple_service_server = bumper_bot_py.simple_service_server:main",
            "simple_service_client = bumper_bot_py.simple_service_client:main",
            "simple_tf_service = bumper_bot_py.simple_tf_service:main",
            "euler_to_quaternion = bumper_bot_py.euler_to_quaternion:main",
            "simple_publisher = bumper_bot_py.simple_publisher:main",
            "simple_subscriber = bumper_bot_py.simple_subscriber:main"
        ],
    },
)
