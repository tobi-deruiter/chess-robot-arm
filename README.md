# Chess-Playing 5DoF Robot Arm
(Made in November 2023)

This is a project I made with a partner as a final project in MFET 348 at Purdue University.

![alt Robot Arm Image](https://github.com/tobi-deruiter/chess-robot-arm/blob/main/chess_robot_arm.png?raw=true)

## Purpose
We made this robot arm to show our understanding of DH parameters, trajectory planning, and inverse kinematics.

## What We Did
We designed, printed, assembled, and programmed a robot arm with 5 degrees of freedom to mimic playing chess against itself.

We programmed the inverse kinematics by hand, after performing the calculations ourselves, in Python. We also used a Python library to generate a virtual chess board and moves for the robot arm to use as reference when mimicing moving chees pieces. The arm is controlled by a Raspberry Pi 3b+ and uses micro servos at the joints to move.

![alt Robot Arm Image](https://github.com/tobi-deruiter/chess-robot-arm/blob/main/chess_robot_arm.mp4?raw=true)
