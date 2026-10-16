# Joint control demonstration

The simulator already loads Gazebo Sim's `JointTrajectoryController` system
from the robot Xacro. `ros_gz_bridge` maps ROS
`trajectory_msgs/msg/JointTrajectory` to Gazebo `gz.msgs.JointTrajectory` on
`/joint_trajectory`. The optional demo publishes low-amplitude trajectories
around the configured standing pose. It is not included in the regular
simulator launch.

## Build

From the workspace root:

```bash
source /opt/ros/lyrical/setup.bash
colcon build --packages-select quad_gazebo --symlink-install
source install/setup.bash
```

## Run

In one terminal, start the simulator as usual:

```bash
ros2 launch quad_gazebo sim.launch.py
```

In a second terminal, source the workspace and explicitly start the demo:

```bash
source /opt/ros/lyrical/setup.bash
source ~/quad_ws/install/setup.bash
ros2 launch quad_gazebo joint_demo.launch.py
```

The node sends a two-point trajectory that moves over four seconds and returns
over the next four seconds. The hip, thigh, and knee offsets are at most
0.04, 0.10, and 0.12 radians from the Xacro initial positions (0, -0.75, 1.5).
These targets are within the respective joint limits. It uses simulation time,
so the demo pauses when Gazebo is paused.

To check that the command stream is active, in another terminal run:

```bash
ros2 topic echo /joint_trajectory
```

Press Ctrl-C in the demo terminal to stop publishing; the simulated controller
holds the last commanded position. Press Ctrl-C in the simulator terminal to
stop Gazebo.
