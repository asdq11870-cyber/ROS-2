import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/unknown/ROS2_Workspaces/bumperbot_ws/install/bumper_bot_py'
