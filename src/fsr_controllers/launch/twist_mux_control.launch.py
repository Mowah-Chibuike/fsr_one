import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    fsr_controllers_pkg = get_package_share_directory("fsr_controllers")
    use_sim_time_arg = DeclareLaunchArgument("use_sim_time", default_value="True", description="Use simulated time")

    teleop_keyboard = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        output="screen",
        prefix="xterm -e",
        parameters=[{
            "stamped": True,
            "frame_id": "base_link",
            "use_sim_time": LaunchConfiguration("use_sim_time")
        }],
        remappings=[
            ("cmd_vel", "/input_key/cmd_vel_stamped")
        ]
    )

    twist_mux_launch = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("twist_mux"),
            "launch",
            "twist_mux_launch.py"
        ),
        launch_arguments={
            "cmd_vel_out": "diffbot_base_controller/cmd_vel_unstamped",
            "config_topics": os.path.join(fsr_controllers_pkg, "config", "twist_mux_topics.yaml"),
            "config_locks": os.path.join(fsr_controllers_pkg, "config", "twist_mux_locks.yaml"),
            "config_joy": os.path.join(fsr_controllers_pkg, "config", "twist_mux_joy.yaml"),
            "use_sim_time": LaunchConfiguration("use_sim_time")
        }.items()
    )

    twist_relay_node = Node(
        package="fsr_controllers",
        executable="twist_relay",
        name="twist_relay",
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}]
    )

    return LaunchDescription([
        use_sim_time_arg,
        teleop_keyboard,
        twist_mux_launch,
        twist_relay_node
    ])