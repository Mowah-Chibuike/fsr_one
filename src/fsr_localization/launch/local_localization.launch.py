from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    robot_localization = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[os.path.join(get_package_share_directory("fsr_localization"), "config", "ekf.yaml"), {"use_sim_time": True}]
    )

    imu_covariance_py = Node(
        package="fsr_localization",
        executable="imu_covariance.py",
        parameters=[
            {'use_sim_time': True}
        ]
    )

    return LaunchDescription([
        robot_localization,
        imu_covariance_py
    ])