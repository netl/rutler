#!/usr/bin/env bash

/usr/bin/tmux new-session -d -s ROS2 
/usr/bin/tmux send-keys -t ROS2.0 '/usr/bin/env bash' Enter
/usr/bin/tmux send-keys -t ROS2.0 'source /opt/ros/jazzy/setup.bash' Enter
/usr/bin/tmux send-keys -t ROS2.0 'cd ros2_ws' Enter
/usr/bin/tmux send-keys -t ROS2.0 'source install/setup.bash' Enter
/usr/bin/tmux send-keys -t ROS2.0 'lsusb' Enter
sleep 60 #wait for permission for webcam
/usr/bin/tmux send-keys -t ROS2.0 'ros2 launch launch_rutler_rc.py' Enter

agetty -h /dev/ttyUSB0 19200 
