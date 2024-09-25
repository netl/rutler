from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='can_rover',
            executable='can_rover',
            parameters=[
                {"voltage_scale":0.0045},
                {"voltage_offset":0.0},
                {"current_scale":-0.0097},
                {"current_offset":13.527}
            ],
        ),
        Node(
            package='rutler',
            executable='pt_gimbal',
        ),
        Node(
            package='rutler',
            executable='joystick_rutler',
        ),
        Node(
            package='joy',
            executable='joy_node',
        ),
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
        ),
    ])
