# Quadruped Robot Simulation using ROS 2 and Gazebo

## Overview

This project demonstrates a quadruped robot simulation using ROS 2
and Gazebo Sim. The robot is spawned in a simulated environment,
performs leg joint animation, and follows a ball along a predefined path.

## Features

- Quadruped robot model described using URDF/Xacro
- Gazebo simulation environment
- ROS 2 and Gazebo communication through a bridge
- Leg joint animation
- Scripted ball-following demonstration

## Technologies

- Ubuntu
- ROS 2 Lyrical
- Gazebo Sim 10
- URDF/Xacro
- Python
- ros_gz bridge

## Project Structure

- `quad_description/`: Robot description and URDF/Xacro files
- `quad_gazebo/`: Simulation world, launch files, configuration,
  and Python scripts

## Prerequisites

Install a compatible environment containing ROS 2 Lyrical and
Gazebo Sim 10, together with the dependencies required by the packages.

## Build

Clone this repository into the `src` directory of a ROS 2 workspace.

From the workspace root, build the packages:

```bash
colcon build --symlink-install
Ipsa Pratibimbita
