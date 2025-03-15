# Gazebo docs

## Setup
**NOTE:** There is absolutely no guarantee that this will work for you

Make sure you have an X server installed. If you're on Linux, it should be there
already. If you're not on Linux, have fun :)

Now, build the docker container:
```bash
docker compose up --build
```
If there are errors try commenting out lines in the `compose.yml` file. 
Or, just message me :)

## Usage
Enter the docker container using
```bash
./enter.sh
```
This will put you in a bash shell. There is a preliminary VSCode devcontainer
configuration, but it does not work in my experience.

### Launch Gazebo
There is a little tool to make launching gazebo more convenient.

In the container, run
```bash
gzl
```
This will open a little box. Click the `Select SDF File` button, then navigate
to `/home/vscode/Worlds`. Inside there are a variety of Gazebo worlds.
The most interesting one is `MovingRobot.sdf`.

Now click `Launch in Gazebo` to open the scene in Gazebo. The little box 
will stay up, and is useful for restarting gazebo.

### Development Workflow
Gazebo has no form of hot reloading. And configuring Gazebo's GUI is
rather difficult. I'll do it at some point...

I edit my sdf scenes in an external program (Outside of the container). When I want
to view my changes, I close Gazebo, and launch it again from the little tool.

**DO NOT RUN MULTIPLE INSTANCES OF GAZEBO AT THE SAME TIME!**
Strange things will happen.

### MovingRobot scene
This scene features a moveable robot with an IMU and an RGBD camera.
The camera is setup to be the same framerate, resolution, and FOV as the Zed Camera 2i.

However, after you open it, you need to do some configuration.

Open the scene. Click on the three dots.
![three dots](imgs/tut1.png)

Add a key listener if you wish to control the robot with the keyboard.
![key listener](imgs/tut2.png)

Add an image viewer so you can see the camera output
![key listener](imgs/tut3.png)

Now, press the start button to start the scene
![key listener](imgs/tut4.png)

Now you should be able to drive aroung the scene using the arrow keys!
![key listener](imgs/tut5.png)

In the image viewer section you can switch to viewing the camera feed instead.

## Connecting to ROS
This section assumes you're in the container.

Setting up custom connections between ROS and Gazebo is easy.
I'm sure you can figure it out.

### MovingRobot scene
Run
```bash
./start_bridge.sh
```
to connect ROS to Gazebo.
The configuration for the gz bridge is in `movingrobot.yaml`.

At some point open the moving robot scene in Gazebo.

The moving robot scene exposes these topics:
 - **/contact**: _GZ to ROS._ When the robot touches something, collision
 info is published here. It includes which objects are colliding.
 - **/camera/image**: _GZ to ROS._ Publishes the images the RGB camera on the robot sees.
 - **/camera/depth_image**: _GZ to ROS._ Publishes the images the depth camera on the robot sees.
 - **/imu**: _GZ to ROS._ Publishes IMU data. This includes the angular velocity and linear acceleration.
 - **/cmd_vel**: _ROS to GZ._ This is how the robot is controlled. You can set the linear velocity and angular velocity here.

### Using rqt
ROS has a nice GUI tool to help see nodes and topics.

You can run it from inside the container with
```bash
rqt
```
Note that Gazebo topics will only publish data when the simulation is running

#### To view images:
In the menu bar, click `Plugins > Visualization > Image View`. On the image view, use the dropdown
at the top left to select an image topic (such as `/camera/image`).

#### To view topics:
In the menu bar, click `Plugins > Topics > Topic Monitor`. Check the checkmark next to the topics 
you want to monitor. You can expand them to get more info. To see their values, scroll all the way to the right
until you see the `Value` column. Note that it takes a second before values start appearing.

#### To publish to topics:
In the menu bar, click `Plugins > Topics > Message Publisher`. At the top, select the topic you
want to publish to, how often you want to send it (frequency), then click the `+` button.

You can then modify the values by double clicking on the `expression` cells.
Once you want to send it, check the checkbox and it'll be sent at the frequency you specified.

