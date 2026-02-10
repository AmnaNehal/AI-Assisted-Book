# Quickstart Guide: Digital Twin (Gazebo & Unity) Module

**Feature**: Module 2 – The Digital Twin (Gazebo & Unity)
**Date**: 2025-12-18
**Audience**: AI and robotics students, educators
**Previous Stage**: data-model.md → **Next Stage**: tasks.md

## Overview

This quickstart guide provides a rapid path to understanding and implementing digital twin concepts using Gazebo, Unity, and ROS 2. Students will learn to create physics simulations, visualize environments, and integrate sensor systems through hands-on examples.

## Prerequisites

### System Requirements
- **Operating System**: Ubuntu 22.04 LTS, Windows 10/11, or macOS 12+
- **RAM**: Minimum 8GB (16GB recommended for Unity development)
- **Storage**: 10GB free space for simulation environments
- **Graphics**: OpenGL 3.3+ compatible GPU for Unity visualization

### Software Dependencies
1. **ROS 2 Humble Hawksbill** (LTS version for Ubuntu 22.04)
2. **Gazebo Harmonic** (LTS simulation environment)
3. **Unity 2022.3 LTS** (with Universal Render Pipeline)
4. **Node.js v18+** (for Docusaurus documentation)
5. **Git** (for version control and content access)

### Installation Check
Verify installations with:
```bash
# ROS 2
source /opt/ros/humble/setup.bash && ros2 --version

# Gazebo
gz version

# Node.js
node --version && npm --version
```

## Getting Started Path

### Phase 1: Physics Simulation with Gazebo (30 minutes)
1. **Launch Basic Simulation**
   ```bash
   # Navigate to simulation workspace
   cd ~/digital-twin-workspace
   source /opt/ros/humble/setup.bash
   ros2 launch gazebo_ros empty_world.launch.py
   ```

2. **Spawn Humanoid Robot Model**
   ```bash
   ros2 run gazebo_ros spawn_entity.py -entity my_robot -file ./models/humanoid.urdf
   ```

3. **Test Physics Interactions**
   - Apply forces to the robot model
   - Observe collision detection
   - Test gravity and dynamics simulation

### Phase 2: High-Fidelity Environments with Unity (45 minutes)
1. **Initialize Unity Project**
   ```bash
   # Create new Unity project for simulation
   unity-hub install 2022.3.22f1
   unity-hub new-project --name DigitalTwinSim --template 3D
   ```

2. **Import Robotics Assets**
   - Import Unity Robotics Hub package
   - Add ROS-TCP-Connector to project
   - Configure network communication settings

3. **Create Basic Environment**
   - Set up lighting and materials
   - Import humanoid robot model
   - Configure camera viewpoints

### Phase 3: Sensor Simulation for Humanoids (60 minutes)
1. **Configure LiDAR Simulation**
   ```xml
   <!-- Add to URDF model -->
   <gazebo reference="lidar_link">
     <sensor type="ray" name="lidar_sensor">
       <ray>
         <scan><horizontal><samples>720</samples></horizontal></scan>
       </ray>
       <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
         <topic_name>laser_scan</topic_name>
       </plugin>
     </sensor>
   </gazebo>
   ```

2. **Test Sensor Data Flow**
   ```bash
   # Monitor sensor topics
   ros2 topic echo /laser_scan sensor_msgs/msg/LaserScan
   ```

3. **Validate Perception Pipeline**
   - Verify sensor data publishing to ROS 2
   - Test perception algorithm integration
   - Confirm data accuracy and timing

## Essential Commands

### Docusaurus Documentation Server
```bash
# Navigate to documentation directory
cd frontend_book
npm install
npm start
```

### Simulation Environment Control
```bash
# Start Gazebo simulation
ros2 launch gazebo_ros empty_world.launch.py

# Reset simulation state
gz service -s /world/empty/reset_simulation --req-type gz.msgs.Empty --rep-type gz.msgs.Boolean

# Stop all simulation processes
pkill -f gz
```

### ROS 2 Communication Monitoring
```bash
# List active topics
ros2 topic list

# Monitor specific topic
ros2 topic echo /sensor_data --field data

# Check node connections
ros2 node list
```

## Common Starting Examples

### Basic Physics Simulation
Create a simple world file to understand Gazebo physics:
```xml
<?xml version="1.0"?>
<sdf version="1.7">
  <world name="physics_demo">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://sun</uri>
    </include>
  </world>
</sdf>
```

### Unity-ROS 2 Bridge Setup
Configure the TCP connector in Unity:
```csharp
// ROS Connection Manager
using ROS2;
using Unity.Robotics.ROSTCPConnector;

public class DigitalTwinConnector : MonoBehaviour
{
    ROSConnection ros;

    void Start()
    {
        ros = ROSConnection.instance;
        ros.RegisterPublisher<LaserScanMsg>("/unity_laser_scan");
    }
}
```

## Troubleshooting Quick Fixes

### Simulation Not Starting
- Check ROS 2 environment sourcing: `source /opt/ros/humble/setup.bash`
- Verify Gazebo installation: `which gz`
- Ensure no conflicting processes: `pkill -f gz`

### Unity-ROS Connection Issues
- Verify TCP connector IP settings match ROS 2 network
- Check firewall settings for port 10000
- Confirm ROS 2 bridge node is running

### Documentation Build Errors
- Update Node.js to v18+: `nvm install 18 && nvm use 18`
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Next Steps

After completing this quickstart, proceed to the full chapters:
1. **Physics Simulation with Gazebo**: Deep dive into physics engines and realistic simulation
2. **High-Fidelity Environments with Unity**: Advanced visualization and interaction techniques
3. **Sensor Simulation for Humanoids**: Comprehensive sensor integration and perception testing

## Resource Links

- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Gazebo Harmonic Tutorials](https://gazebosim.org/tutorials)
- [Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)
- [Digital Twin Module Index](./index.md)

## Support and Community

- **Issue Tracker**: Report problems with the educational content
- **Discussion Forum**: Engage with other students learning digital twin concepts
- **Office Hours**: Weekly virtual sessions for Q&A and troubleshooting