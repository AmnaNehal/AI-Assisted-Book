---
title: Humanoid Modeling with URDF
sidebar_position: 3
description: Robot modeling using Unified Robot Description Format
tags: [ros2, robotics, ai, urdf]
---

# Humanoid Modeling with URDF

## Learning Objectives

By the end of this chapter, you should be able to:
- Explain the purpose and structure of URDF (Unified Robot Description Format)
- Describe the concepts of links, joints, and kinematics in robot modeling
- Understand how URDF enables both simulation and control of robots
- Identify the role of URDF in humanoid robot development

## Introduction

URDF (Unified Robot Description Format) is the standard format for describing robot structure in ROS. It provides a way to represent the physical and visual properties of a robot, including its links (rigid bodies), joints (connections between links), and other properties such as inertia, visual appearance, and collision properties. URDF is essential for both simulation and real-world robot control.

## Purpose of URDF

![URDF Structure](/img/urdf-modeling/urdf-structure.txt)

URDF serves several critical purposes in robotics:

### Robot Description
URDF provides a complete description of a robot's physical structure, including:
- The arrangement of links and joints
- Physical properties like mass and inertia
- Visual and collision models
- Kinematic relationships between different parts

### Simulation Interface
URDF enables robots to be accurately simulated in environments like Gazebo by providing all necessary physical properties for physics calculations.

### Control System Integration
URDF provides the kinematic model that control systems use to understand how joint movements affect the position of robot parts, enabling precise control.

### Visualization
URDF descriptions allow tools to visualize robots in 3D, helping developers understand and debug robot behavior.

## Links, Joints, and Kinematics

### Links

Links in URDF represent rigid bodies in the robot structure. Each link has properties such as:
- **Mass**: The mass of the link
- **Inertia**: The inertial properties that affect how the link responds to forces
- **Visual**: How the link appears visually (shape, color, texture)
- **Collision**: How the link behaves in collision detection (shape for collision checking)

Links are connected by joints to form the complete robot structure.

### Joints

Joints define the connections between links and specify how they can move relative to each other. The main types of joints include:
- **Revolute**: A hinge joint that rotates around a single axis
- **Continuous**: Like revolute but with unlimited rotation
- **Prismatic**: A sliding joint that moves linearly along an axis
- **Fixed**: A joint that rigidly connects two links (no movement)
- **Floating**: A joint that allows motion in all 6 degrees of freedom
- **Planar**: A joint that allows motion in a plane

Each joint has properties like limits, dynamics, and safety controllers.

### Kinematics

Kinematics in URDF refers to the study of motion without considering forces. It includes:
- **Forward Kinematics**: Calculating the position of end-effectors given joint angles
- **Inverse Kinematics**: Calculating required joint angles to achieve a desired end-effector position
- **Kinematic Chains**: Sequences of joints and links that connect a base to an end-effector

URDF provides the structure needed for kinematic calculations, which are essential for robot control and planning.

## URDF's Role in Simulation and Control

### Simulation

In simulation environments like Gazebo, URDF serves as the input for creating accurate robot models. The physical properties defined in URDF are used to:
- Calculate how forces affect robot movement
- Determine collision responses
- Simulate sensor data based on robot position and orientation
- Enable realistic robot behavior in virtual environments

### Control

For real robot control, URDF provides:
- The kinematic model needed for motion planning
- Information about joint limits and constraints
- Mass properties needed for dynamics calculations
- The relationship between joint space and Cartesian space

Control algorithms use this information to generate appropriate commands for achieving desired robot behaviors.

## Summary

URDF is fundamental to robotics in the ROS ecosystem, providing a standardized way to describe robot structure and properties. Understanding links, joints, and kinematics is essential for working with humanoid robots and other complex robotic systems. URDF enables both accurate simulation and effective control of robots.

## Key Takeaways

- URDF (Unified Robot Description Format) is the standard for describing robot structure in ROS
- Links represent rigid bodies, joints define connections and movement between links
- Kinematics involves the study of motion and is essential for robot control
- URDF enables both simulation and control by providing complete robot models
- The format is essential for humanoid robot development and integration

## References and Further Reading

- [URDF Documentation](http://wiki.ros.org/urdf)
- [URDF Tutorials](http://wiki.ros.org/urdf/Tutorials)
- [Working with URDF in ROS 2](https://docs.ros.org/en/rolling/Tutorials/URDF/Using-URDF-with-Robot-State-Publisher.html)
- [xacro: XML Macros for URDF](http://wiki.ros.org/xacro)