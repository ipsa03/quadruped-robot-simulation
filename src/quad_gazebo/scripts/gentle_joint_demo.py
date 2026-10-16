#!/usr/bin/env python3

"""Simple alternating diagonal gait for the quadruped."""

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class GentleJointDemo(Node):
    LEGS = ("fl", "fr", "rl", "rr")
    JOINTS = [
        f"{leg}_{joint}_joint"
        for leg in LEGS
        for joint in ("hip", "thigh", "knee")
    ]

    HOME = (0.0, -0.75, 1.5)
    HIP_SWING = 0.08
    THIGH_SWING = 0.12
    KNEE_SWING = 0.16
    STEP_SECONDS = 2

    # Opposite diagonal pairs alternate their joint targets.
    LEG_SIGNS = (1.0, -1.0, -1.0, 1.0)

    def __init__(self):
        super().__init__("gentle_joint_demo")
        self.publisher = self.create_publisher(
            JointTrajectory, "/joint_trajectory", 10
        )
        self.phase = 0
        self.timer = self.create_timer(0.5, self.wait_for_bridge)
        self.get_logger().info("Waiting for the trajectory bridge.")

    def wait_for_bridge(self):
        if self.publisher.get_subscription_count() == 0:
            return

        self.timer.cancel()
        self.publish_cycle()
        self.timer = self.create_timer(4.5, self.publish_cycle)
        self.get_logger().info(
            "Sending alternating diagonal-leg trajectories. Ctrl-C stops."
        )

    def pose(self, direction):
        positions = []
        for sign in self.LEG_SIGNS:
            positions.extend((
                sign * direction * self.HIP_SWING,
                self.HOME[1] + direction * self.THIGH_SWING,
                self.HOME[2] - direction * self.KNEE_SWING,
            ))
        return positions

    def publish_cycle(self):
        direction = 1.0 if self.phase % 2 == 0 else -1.0
        trajectory = JointTrajectory()
        trajectory.joint_names = self.JOINTS

        for d, seconds in ((direction, self.STEP_SECONDS),
                           (-direction, 2 * self.STEP_SECONDS)):
            point = JointTrajectoryPoint()
            point.positions = self.pose(d)
            point.time_from_start.sec = seconds
            trajectory.points.append(point)

        self.publisher.publish(trajectory)
        self.phase += 1


def main(args=None):
    rclpy.init(args=args)
    node = GentleJointDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
