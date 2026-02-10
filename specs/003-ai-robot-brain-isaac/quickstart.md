# Quickstart Guide: AI-Robot Brain (NVIDIA Isaac™) Module

**Feature**: Module 3 – The AI-Robot Brain (NVIDIA Isaac™)
**Date**: 2025-12-18
**Audience**: AI and robotics students, educators
**Previous Stage**: data-model.md → **Next Stage**: tasks.md

## Overview

This quickstart guide provides a rapid path to understanding and implementing AI-robot brain concepts using NVIDIA Isaac Sim, Isaac ROS, and Nav2. Students will learn to create photorealistic simulations, build hardware-accelerated perception pipelines, and implement navigation systems through hands-on examples.

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 22.04 LTS, Windows 10/11 (with WSL2), or macOS 12+ (with Docker)
- **GPU**: NVIDIA GPU with CUDA support (RTX 2060 or better recommended)
- **RAM**: Minimum 16GB (32GB recommended for Isaac Sim)
- **Storage**: 20GB free space for Isaac ecosystem
- **CUDA**: CUDA 11.8+ with compatible NVIDIA drivers

### Software Dependencies
1. **ROS 2 Humble Hawksbill** (LTS version for Ubuntu 22.04)
2. **NVIDIA Isaac Sim 2023.1+** (with Omniverse support)
3. **Isaac ROS 3.0+** (with perception accelerations)
4. **Nav2** (navigation stack for ROS 2)
5. **Node.js v18+** (for Docusaurus documentation)
6. **Docker** (for containerized Isaac applications)

### Installation Check
Verify installations with:
```bash
# ROS 2
source /opt/ros/humble/setup.bash && ros2 --version

# CUDA
nvidia-smi && nvcc --version

# Isaac Sim (check if Omniverse app launcher is available)
omniverse-app-launcher --version
```

## Getting Started Path

### Phase 1: NVIDIA Isaac Sim (45 minutes)
1. **Launch Isaac Sim**
   ```bash
   # Start Isaac Sim from Omniverse
   cd ~/isaac-sim && ./isaac-sim.launch.sh
   ```

2. **Load Humanoid Robot Model**
   ```bash
   # In Isaac Sim interface, load humanoid robot
   # Select robot from Isaac Sim robot library
   ```

3. **Create Photorealistic Environment**
   - Select environment from Isaac Sim assets
   - Configure lighting and materials for realism
   - Test physics simulation of humanoid model

### Phase 2: Isaac ROS and Perception (60 minutes)
1. **Initialize Perception Pipeline**
   ```bash
   # Navigate to Isaac ROS workspace
   cd ~/isaac-ros-dev && source /opt/ros/humble/setup.bash
   ros2 launch isaac_ros_pointcloud_utils pointcloud_to_occupancy_grid.launch.py
   ```

2. **Configure Hardware-Accelerated Perception**
   ```bash
   # Launch CUDA-accelerated object detection
   ros2 launch isaac_ros_detectnet isaac_ros_detectnet.launch.py
   ```

3. **Test Visual SLAM Integration**
   ```bash
   # Launch Isaac ROS Visual SLAM
   ros2 launch isaac_ros_visual_slam visual_slam.launch.py
   ```

### Phase 3: Navigation with Nav2 (75 minutes)
1. **Configure Nav2 for Humanoid Movement**
   ```bash
   # Launch Nav2 with Isaac perception integration
   ros2 launch nav2_bringup navigation_launch.py
   ```

2. **Set Up Perception-Planning-Action Loop**
   ```bash
   # Launch complete loop with perception, planning, and action
   ros2 launch ai_robot_brain complete_system.launch.py
   ```

3. **Test Navigation in Isaac Sim Environment**
   - Send navigation goals to humanoid robot
   - Observe perception → planning → action flow
   - Validate path planning and obstacle avoidance

## Essential Commands

### Docusaurus Documentation Server
```bash
# Navigate to documentation directory
cd frontend_book
npm install
npm start
```

### Isaac Sim Control
```bash
# Start Isaac Sim in headless mode
./isaac-sim.headless.sh

# Reset simulation state
# Use Isaac Sim UI or Omniverse commands
```

### ROS 2 Communication Monitoring
```bash
# List active topics
ros2 topic list

# Monitor perception topics
ros2 topic echo /isaac_ros/detections --field results

# Check node connections
ros2 node list
```

## Common Starting Examples

### Basic Isaac Sim Scene
Create a simple scene for humanoid robot training:
```python
# Python script to create Isaac Sim environment
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage

# Create world instance
world = World(stage_units_in_meters=1.0)

# Add humanoid robot to stage
assets_root_path = get_assets_root_path()
add_reference_to_stage(
    usd_path=assets_root_path + "/Isaac/Robots/Humanoid/humanoid.usd",
    prim_path="/World/Humanoid"
)

# Play the simulation
world.play()
```

### Isaac ROS Perception Pipeline
Configure a basic perception pipeline:
```xml
<!-- Launch file for Isaac ROS perception -->
<launch>
  <!-- Camera input -->
  <node pkg="isaac_ros_image_proc" exec="rectify_node" name="rectify_node">
    <param name="input_width" value="1920"/>
    <param name="input_height" value="1080"/>
  </node>

  <!-- Object detection -->
  <node pkg="isaac_ros_detectnet" exec="isaac_ros_detectnet" name="detectnet">
    <param name="model_name" value="resnet18_detector"/>
  </node>
</launch>
```

## Troubleshooting Quick Fixes

### Isaac Sim Not Starting
- Check NVIDIA GPU and CUDA installation: `nvidia-smi`
- Verify Isaac Sim dependencies are met
- Ensure sufficient RAM and storage space

### Perception Pipeline Issues
- Check CUDA acceleration: `nvidia-smi`
- Verify Isaac ROS packages are installed
- Confirm GPU memory is sufficient for processing

### Documentation Build Errors
- Update Node.js to v18+: `nvm install 18 && nvm use 18`
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Next Steps

After completing this quickstart, proceed to the full chapters:
1. **NVIDIA Isaac Sim**: Deep dive into photorealistic simulation and synthetic data generation
2. **Isaac ROS and Perception**: Advanced hardware-accelerated perception and VSLAM
3. **Navigation with Nav2**: Complete perception → planning → action loop implementation

## Resource Links

- [NVIDIA Isaac Sim Documentation](https://docs.omniverse.nvidia.com/isaacsim/latest/index.html)
- [Isaac ROS Documentation](https://nvidia-isaac-ros.github.io/index.html)
- [Nav2 Documentation](https://navigation.ros.org/)
- [AI-Robot Brain Module Index](./index.md)

## Support and Community

- **Issue Tracker**: Report problems with the educational content
- **Discussion Forum**: Engage with other students learning Isaac technologies
- **Office Hours**: Weekly virtual sessions for Q&A and troubleshooting