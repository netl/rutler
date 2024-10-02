from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='can_rover',
            executable='can_rover',
            parameters=[
                {"voltage_scale":0.00455},
                {"voltage_offset":0.0},
                {"current_scale":-0.0097},
                {"current_offset":13.527}
            ],
            remappings=[
                ('/rover/channel_1', '/rover/accelerator'),
                ('/rover/channel_2', '/rover/steering'),
                ('/rover/channel_3', '/rover/tilt'),
                ('/rover/channel_4', '/rover/pan'),
            ],
        ),
        Node(
            package='rutler',
            executable='pt_gimbal',
            remappings=[
                ('/rover/channel_3', '/rover/tilt'),
                ('/rover/channel_4', '/rover/pan'),
            ],
        ),
        Node(
            package='rutler',
            executable='joystick_rutler',
        ),
        Node(
            package='rutler',
            executable='face_finder',
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
