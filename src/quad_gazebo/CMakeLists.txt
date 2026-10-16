cmake_minimum_required(VERSION 3.8)
project(quad_gazebo)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY worlds config launch
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
    scripts/gentle_joint_demo.py
    scripts/ball_follow.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
