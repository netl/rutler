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
                {"current_offset":13.5509},
                {"channel_1_scale":700},
                {"channel_2_scale":300},
                {"channel_2_offset":1416},
            ],
            remappings=[
                ('/rover/channel_1', '/rover/accelerator'),
                ('/rover/channel_2', '/rover/steering'),
            ],
        ),
        Node(
            package='rutler',
            executable='twist_rover',
            remappings=[
                ('/accelerator', '/rover/accelerator'),
                ('/steering', '/rover/steering'),
            ],
        ),
        Node(
            package='v4l2_camera',
            executable='v4l2_camera_node',
            remappings=[
                ('/image_raw', '/rover/image_raw'),
                ('/image_info', '/rover/image_info'),
            ],
        ),
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            parameters=[{'channel_type':'serial',
                         'serial_port': '/dev/ttyUSB0', 
                         'serial_baudrate': '460800', 
                         'frame_id': 'laser',
                         'inverted': 'false', 
                         'angle_compensate': 'true', 
                         'scan_mode': 'Standard'}],
            output='screen'),
    ])
