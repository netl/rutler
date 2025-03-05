FROM ros:jazzy-ros-core
WORKDIR /usr/local/ros2_ws

#install needed stuff
RUN apt update
RUN apt install -y git vim python3-rosdep python3-colcon-common-extensions

#copy nodes and launch file
RUN mkdir src
COPY can-rover/ros2_can_rover src/can_rover 
COPY ros-node ./src/rutler
COPY launch_rutler_rc.py ./

#build
SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/jazzy/setup.bash
RUN colcon build
RUN source install/setup.bash

#install dependencies
RUN rosdep init
RUN rosdep update
RUN rosdep install --from-paths src -y --ignore-src

#run ros2 with launch file
CMD source /opt/ros/jazzy/setup.bash; source install/setup.bash; ros2 launch launch_rutler_rc.py
