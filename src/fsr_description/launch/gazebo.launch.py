from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
import os
from os.path import pathsep
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

def generate_launch_description():

    fsr_description_dir = get_package_share_directory("fsr_description")

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(fsr_description_dir, "urdf", "fsr_one.xacro"),
        description="Absolute path to robot URDF file"
    )

    world_name_arg = DeclareLaunchArgument(
        name="world_name",
        default_value="empty"
    )


    world_path = PathJoinSubstitution([
        fsr_description_dir,
        "worlds",
        PythonExpression([
            "'", LaunchConfiguration("world_name"), "' + '.world'"
        ])
    ])

    use_sim_time_arg = DeclareLaunchArgument(
            name="use_sim_time",
            default_value="True",
            description="Use Gazebo sim time"
        )

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model"),]), value_type=str)

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description,
             "use_sim_time": use_sim_time
            }
        ]
    )

    model_path = str(Path(fsr_description_dir).parent.resolve())
    model_path += pathsep + os.path.join(fsr_description_dir, "models")

    gazebo_resource_path = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH", model_path
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            )
        ]),
        launch_arguments={
            "gz_args": PythonExpression([
                "'", world_path, " -v 4 -r'"
            ])
        }.items()
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description", "-name", "fsr_one_robot", "-z", "0.1"]
    )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU"
        ],
        remappings=[
            ("/imu", "/imu/out")
        ],
        output="screen"
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen"
    )

    diff_drive_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diffbot_base_controller"],
        output="screen"
    )

    after_spawn = RegisterEventHandler(
    OnProcessExit(target_action=gz_spawn_entity, on_exit=[joint_state_broadcaster_spawner]))
    after_broad = RegisterEventHandler(
    OnProcessExit(target_action=joint_state_broadcaster_spawner, on_exit=[diff_drive_controller_spawner]))

    return LaunchDescription([
        model_arg,
        world_name_arg,
        use_sim_time_arg,
        robot_state_publisher,
        gazebo_resource_path,
        gazebo,
        gz_spawn_entity,
        gz_ros2_bridge,
        after_spawn,
        after_broad
    ])