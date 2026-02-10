# Humanoid Robotics Education

This educational website covers humanoid robotics concepts including ROS 2 as middleware, Gazebo physics simulation, Unity visualization, and digital twin technologies. It serves as a comprehensive guide for AI and robotics students to understand the complete robotics development pipeline.

## About

This documentation site includes two comprehensive modules:

### Module 1: ROS 2 Nervous System
Understanding ROS 2 as middleware for AI agents and humanoid robot controllers, covering:
- ROS 2 Fundamentals: Core concepts of ROS 2 as middleware for AI agents and humanoid robot controllers
- Python Agents to ROS 2: How Python AI agents communicate with ROS 2 using rclpy
- Humanoid Modeling with URDF: Robot modeling using Unified Robot Description Format

### Module 2: Digital Twin (Gazebo & Unity)
Building digital twins of humanoid robots to simulate physics, environments, and human-robot interaction, covering:
- Physics Simulation with Gazebo: Role of simulation in Physical AI, physics engines, and ROS 2 integration
- High-Fidelity Environments with Unity: Visual realism and human-robot interaction concepts
- Sensor Simulation for Humanoids: Simulating LiDAR, depth cameras, and IMUs for perception testing

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> yarn deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.
