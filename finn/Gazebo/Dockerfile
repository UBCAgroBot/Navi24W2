FROM agrobotappliedai/ros-containers:gazebo

RUN apt-get update
RUN apt-get install -y python3 python3-tk
RUN apt-get install -y ros-humble-rqt-common-plugins ros-humble-rqt
COPY ./gazebo_launcher.py /home/vscode/gazebo_launcher.py

