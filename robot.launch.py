from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_simulator',
            executable='robot_node',
            name='robot_node',
            output='screen'
        ),
        Node(
            package='robot_simulator',
            executable='viz_node',
            name='viz_node',
            output='screen'
        ),
        Node(
            package='robot_simulator',
            executable='controller_node',
            name='controller_node',
            output='screen'
        ),
    ])
