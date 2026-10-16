#!/usr/bin/env python3

import subprocess
import time

BALL_NAME = "ball"
ROBOT_NAME = "quad"

BALL_START_X = 2.5
BALL_END_X = 3.0
ROBOT_START_X = 1.7

BALL_Z = 0.1
ROBOT_Z = 0.25

STEP = 0.03
DELAY = 0.15


def set_pose(name, x, z):
    request = (
        f'name: "{name}", '
        f'position: {{x: {x}, y: 0, z: {z}}}, '
        'orientation: {w: 1}'
    )

    result = subprocess.run(
        [
            "gz", "service",
            "-s", "/world/ball_world/set_pose",
            "--reqtype", "gz.msgs.Pose",
            "--reptype", "gz.msgs.Boolean",
            "--timeout", "2000",
            "--req", request,
        ],
        capture_output=True,
        text=True,
        timeout=3,
    )

    if result.returncode != 0:
        print(f"Gazebo error moving {name}: {result.stderr.strip()}")
        return False

    print(f"Moved {name} to x={x:.2f}")
    return True


def main():
    ball_x = BALL_START_X
    robot_x = ROBOT_START_X

    print("Ball-follow demo starting. Press Ctrl+C to stop.")

    try:
        while ball_x < BALL_END_X:
            ball_x += STEP

            # Keep the robot behind the ball.
            target_robot_x = ball_x - 0.6

            if robot_x < target_robot_x:
                robot_x = min(robot_x + STEP, target_robot_x)

            if not set_pose(BALL_NAME, ball_x, BALL_Z):
                break

            if not set_pose(ROBOT_NAME, robot_x, ROBOT_Z):
                break

            time.sleep(DELAY)

        print("Demo finished.")

    except KeyboardInterrupt:
        print("\nDemo stopped.")


if __name__ == "__main__":
    main()
