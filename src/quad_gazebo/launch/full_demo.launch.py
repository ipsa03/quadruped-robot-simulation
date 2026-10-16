import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    gz_share = get_package_share_directory('quad_gazebo')
    desc_share = get_package_share_directory('quad_description')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    xacro_file = os.path.join(
        desc_share, 'urdf', 'quad.urdf.xacro'
    )
    world = os.path.join(
        gz_share, 'worlds', 'ball_world.sdf'
    )
    bridge_yaml = os.path.join(
        gz_share, 'config', 'bridge.yaml'
    )

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_sim, 'launch', 'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r {world}'
        }.items()
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'ball_world',
            '-topic', 'robot_description',
            '-name', 'quad',
            '-z', '0.30'
        ],
        output='screen'
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_yaml,
            'use_sim_time': True
        }],
        output='screen'
    )

    leg_demo = Node(
        package='quad_gazebo',
        executable='gentle_joint_demo.py',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    ball_follow = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='quad_gazebo',
                executable='ball_follow.py',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        gz_sim,
        rsp,
        spawn,
        bridge,
        leg_demo,
        ball_follow
    ])
