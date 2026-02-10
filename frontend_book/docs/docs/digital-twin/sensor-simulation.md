---
title: Sensor Simulation for Humanoids
sidebar_label: Sensor Simulation
description: Simulating various sensors for humanoid robots in digital twin environments
keywords:
  - Sensor Simulation
  - Digital Twin
  - Humanoid Robots
  - LiDAR
  - Depth Cameras
  - IMU
  - ROS 2
---

# Sensor Simulation for Humanoids

## Overview

Sensor simulation is a critical component of digital twin environments for humanoid robots, enabling the testing of perception algorithms and sensor fusion techniques without the risks and costs associated with real hardware. This chapter explores how to simulate various sensors commonly found on humanoid robots and how to integrate their data into ROS 2 for comprehensive testing.

## Types of Sensors in Humanoid Robots

Humanoid robots typically employ multiple sensor types to perceive their environment:

### LiDAR Sensors
LiDAR (Light Detection and Ranging) sensors are essential for humanoid robots due to their ability to create accurate 2D and 3D maps of the environment.

**Characteristics:**
- **Range**: Typically 0.1m to 30m effective range
- **Accuracy**: Millimeter-level distance measurements
- **Field of View**: 180° to 360° horizontal coverage
- **Update Rate**: 5-20 Hz for typical robotics applications
- **Data Format**: LaserScan or PointCloud2 messages

**Applications in Humanoid Robots:**
- Navigation and obstacle avoidance
- Environment mapping and localization
- Path planning and collision detection
- Human detection and tracking

### Depth Cameras
Depth cameras provide 3D spatial information, crucial for humanoid robots that need to interact with objects and navigate complex environments.

**Characteristics:**
- **Resolution**: 320×240 to 640×480 pixels
- **Depth Range**: 0.3m to 5m effective range
- **Accuracy**: Millimeter-level depth precision
- **Update Rate**: 15-30 Hz
- **Data Format**: Image messages with depth information

**Applications in Humanoid Robots:**
- Object recognition and manipulation
- 3D scene understanding
- Human pose estimation
- Surface normal estimation

### IMU (Inertial Measurement Unit)
IMUs are critical for humanoid robot stability and balance, providing data about the robot's orientation and motion.

**Characteristics:**
- **Sensors**: 3-axis accelerometer, 3-axis gyroscope, 3-axis magnetometer
- **Update Rate**: 100-1000 Hz for high-performance IMUs
- **Accuracy**: Depends on sensor quality and calibration
- **Data Format**: Imu message type in ROS 2

**Applications in Humanoid Robots:**
- Balance and posture control
- Motion tracking and gait analysis
- Orientation estimation
- Fall detection and recovery

## Simulating LiDAR Sensors

### 2D LiDAR Simulation

Creating a 2D LiDAR sensor in Gazebo involves defining a ray sensor in the URDF model:

```xml
<link name="lidar_link">
  <visual>
    <geometry>
      <cylinder radius="0.05" length="0.04"/>
    </geometry>
    <material name="black"/>
  </visual>
  <collision>
    <geometry>
      <cylinder radius="0.05" length="0.04"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.1"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<joint name="lidar_joint" type="fixed">
  <parent link="base_link"/>
  <child link="lidar_link"/>
  <origin xyz="0 0 1.0" rpy="0 0 0"/>
</joint>

<gazebo reference="lidar_link">
  <sensor type="ray" name="lidar_sensor">
    <always_on>true</always_on>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>720</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>30.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <namespace>/robot1</namespace>
        <remapping>~/out:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
  </sensor>
</gazebo>
```

### 3D LiDAR Simulation

For more advanced humanoid applications, 3D LiDAR simulation provides comprehensive spatial understanding:

```xml
<gazebo reference="lidar_link">
  <sensor type="ray" name="velodyne_sensor">
    <ray>
      <scan>
        <horizontal>
          <samples>800</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
        <vertical>
          <samples>32</samples>
          <resolution>1</resolution>
          <min_angle>-0.436</min_angle>
          <max_angle>0.436</max_angle>
        </vertical>
      </scan>
    </ray>
    <plugin name="velodyne_controller" filename="libgazebo_ros_velodyne_gpu_laser.so">
      <topic_name>points</topic_name>
      <frame_name>lidar_link</frame_name>
      <min_range>0.9</min_range>
      <max_range>100.0</max_range>
      <gaussian_noise>0.008</gaussian_noise>
    </plugin>
  </sensor>
</gazebo>
```

## Simulating Depth Cameras

### RGB-D Camera Simulation

Depth cameras are typically implemented as stereo camera sensors or structured light sensors in simulation:

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.02 0.08 0.04"/>
    </geometry>
    <material name="black"/>
  </visual>
  <collision>
    <geometry>
      <box size="0.02 0.08 0.04"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="0.05"/>
    <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
  </inertial>
</link>

<joint name="camera_joint" type="fixed">
  <parent link="head_link"/>
  <child link="camera_link"/>
  <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="depth" name="camera_sensor">
    <always_on>true</always_on>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>
      <image>
        <format>R8G8B8</format>
        <width>640</width>
        <height>480</height>
      </image>
      <clip>
        <near>0.1</near>
        <far>10</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
      <alwaysOn>true</alwaysOn>
      <updateRate>30.0</updateRate>
      <cameraName>camera</cameraName>
      <imageTopicName>rgb/image_raw</imageTopicName>
      <depthImageTopicName>depth/image_raw</depthImageTopicName>
      <pointCloudTopicName>depth/points</pointCloudTopicName>
      <cameraInfoTopicName>rgb/camera_info</cameraInfoTopicName>
      <depthImageCameraInfoTopicName>depth/camera_info</depthImageCameraInfoTopicName>
      <frameName>camera_link</frameName>
      <baseline>0.1</baseline>
      <distortion_k1>0.0</distortion_k1>
      <distortion_k2>0.0</distortion_k2>
      <distortion_k3>0.0</distortion_k3>
      <distortion_t1>0.0</distortion_t1>
      <distortion_t2>0.0</distortion_t2>
    </plugin>
  </sensor>
</gazebo>
```

### Sensor Noise and Calibration

Realistic sensor simulation includes noise models that reflect actual sensor characteristics:

```xml
<plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
  <!-- ... other parameters ... -->
  <image>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>
    </noise>
  </image>
  <depth_camera>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.01</stddev>
    </noise>
  </depth_camera>
</plugin>
```

## Simulating IMU Sensors

### IMU Configuration in Gazebo

IMU sensors are crucial for humanoid balance and orientation estimation:

```xml
<link name="imu_link">
  <inertial>
    <mass value="0.01"/>
    <inertia ixx="0.0001" ixy="0" ixz="0" iyy="0.0001" iyz="0" izz="0.0001"/>
  </inertial>
</link>

<joint name="imu_joint" type="fixed">
  <parent link="base_link"/>
  <child link="imu_link"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
</joint>

<gazebo reference="imu_link">
  <gravity>true</gravity>
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <visualize>true</visualize>
    <imu>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>2e-4</stddev>
            <bias_mean>0.0000075</bias_mean>
            <bias_stddev>0.0000008</bias_stddev>
          </noise>
        </z>
      </angular_velocity>
      <linear_acceleration>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.1</bias_mean>
            <bias_stddev>0.001</bias_stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.1</bias_mean>
            <bias_stddev>0.001</bias_stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>1.7e-2</stddev>
            <bias_mean>0.1</bias_mean>
            <bias_stddev>0.001</bias_stddev>
          </noise>
        </z>
      </linear_acceleration>
    </imu>
    <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
      <ros>
        <namespace>/robot1</namespace>
        <remapping>~/out:=imu/data</remapping>
      </ros>
      <initial_orientation_as_reference>false</initial_orientation_as_reference>
      <body_name>imu_link</body_name>
    </plugin>
  </sensor>
</gazebo>
```

## Sensor Data Flow into ROS 2

### Topic Architecture

The simulated sensors publish data to ROS 2 topics following standard message formats:

```bash
# LiDAR data
/robot1/scan -> sensor_msgs/LaserScan

# Depth camera data
/robot1/camera/rgb/image_raw -> sensor_msgs/Image
/robot1/camera/depth/image_raw -> sensor_msgs/Image
/robot1/camera/depth/points -> sensor_msgs/PointCloud2

# IMU data
/robot1/imu/data -> sensor_msgs/Imu
```

### Sensor Data Processing Pipeline

A typical sensor data processing pipeline might look like this:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image, Imu
from cv_bridge import CvBridge
import numpy as np

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')

        # Create subscribers for all sensor types
        self.scan_sub = self.create_subscription(
            LaserScan, '/robot1/scan', self.scan_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, '/robot1/imu/data', self.imu_callback, 10)
        self.image_sub = self.create_subscription(
            Image, '/robot1/camera/rgb/image_raw', self.image_callback, 10)

        # Create publisher for fused data
        self.fused_pub = self.create_publisher(
            # Custom fused sensor message, if needed
            'sensor_msgs/CombinedSensorData', '/robot1/sensor_fusion', 10)

        self.bridge = CvBridge()

    def scan_callback(self, msg):
        """Process LiDAR scan data"""
        # Process laser scan for obstacle detection
        ranges = np.array(msg.ranges)
        valid_ranges = ranges[np.isfinite(ranges)]

        # Perform obstacle detection algorithms
        obstacles = self.detect_obstacles(valid_ranges)

        # Store processed data for fusion
        self.last_scan = obstacles

    def imu_callback(self, msg):
        """Process IMU data"""
        # Extract orientation and acceleration
        orientation = msg.orientation
        angular_velocity = msg.angular_velocity
        linear_acceleration = msg.linear_acceleration

        # Process orientation for balance control
        euler_orientation = self.quaternion_to_euler(
            orientation.x, orientation.y, orientation.z, orientation.w)

        # Store processed data for fusion
        self.last_orientation = euler_orientation

    def image_callback(self, msg):
        """Process camera image data"""
        # Convert ROS Image to OpenCV format
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Perform image processing
        processed_image = self.process_image(cv_image)

        # Store processed data for fusion
        self.last_image = processed_image

    def detect_obstacles(self, ranges):
        """Simple obstacle detection from laser ranges"""
        # Implement obstacle detection algorithm
        # This is a simplified example
        min_distance = np.min(ranges)
        obstacle_angles = np.where(ranges < 1.0)[0]  # Objects within 1m

        return {
            'min_distance': min_distance,
            'obstacle_angles': obstacle_angles,
            'obstacle_count': len(obstacle_angles)
        }

    def quaternion_to_euler(self, x, y, z, w):
        """Convert quaternion to Euler angles"""
        # Simplified conversion
        import math

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)

        return (roll, pitch, yaw)

def main(args=None):
    rclpy.init(args=args)
    sensor_fusion_node = SensorFusionNode()

    try:
        rclpy.spin(sensor_fusion_node)
    except KeyboardInterrupt:
        pass
    finally:
        sensor_fusion_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Using Simulated Sensors for Perception Testing

### Perception Algorithm Development

The simulated sensors enable comprehensive testing of perception algorithms:

#### Object Detection Testing

```bash
# Test object detection with synthetic data
ros2 run perception_package object_detector \
  --ros-args \
  -p image_topic:=/robot1/camera/rgb/image_raw \
  -p confidence_threshold:=0.7 \
  -p model_path:=/path/to/model.onnx
```

#### SLAM Testing

```bash
# Test SLAM with simulated sensors
ros2 launch slam_toolbox mapping.launch.py \
  use_sim_time:=true \
  params_file:=/path/to/slam_params.yaml
```

#### Human Detection

```bash
# Test human detection in simulation
ros2 run human_detection human_detector \
  --ros-args \
  -p camera_topic:=/robot1/camera/rgb/image_raw \
  -p lidar_topic:=/robot1/scan
```

### Sensor Fusion Validation

Testing sensor fusion algorithms in simulation allows for:

- **Cross-Validation**: Comparing different sensor outputs
- **Ground Truth**: Access to true robot states for algorithm validation
- **Controlled Scenarios**: Testing specific situations repeatedly
- **Performance Metrics**: Quantitative evaluation of sensor performance

## Practical Example: Humanoid Robot Sensor Suite

A complete sensor configuration for a humanoid robot might include:

```xml
<!-- Head-mounted sensors -->
<gazebo reference="head_link">
  <!-- RGB-D camera for perception -->
  <sensor type="depth" name="head_camera">
    <!-- Camera configuration -->
  </sensor>

  <!-- Infrared sensor for close-range detection -->
  <sensor type="ray" name="head_ir">
    <!-- IR sensor configuration -->
  </sensor>
</gazebo>

<!-- Torso-mounted sensors -->
<gazebo reference="torso_link">
  <!-- IMU for balance -->
  <sensor type="imu" name="torso_imu">
    <!-- IMU configuration -->
  </sensor>

  <!-- Ultrasonic sensors for obstacle detection -->
  <sensor type="ray" name="torso_sonar_left">
    <!-- Sonar configuration -->
  </sensor>
</gazebo>

<!-- Leg-mounted sensors -->
<gazebo reference="l_foot_link">
  <!-- Force/Torque sensors for balance -->
  <sensor type="force_torque" name="left_foot_ft">
    <!-- FT sensor configuration -->
  </sensor>
</gazebo>
```

## Quality Assurance for Sensor Simulation

### Validation Techniques

- **Cross-Validation**: Compare simulated sensor outputs with real sensor data
- **Ground Truth Verification**: Ensure simulated measurements match known environment properties
- **Timing Analysis**: Verify sensor update rates and synchronization
- **Noise Characterization**: Validate that simulated noise matches real sensor characteristics

### Performance Considerations

- **Simulation Speed**: Ensure sensor simulation doesn't slow down physics simulation
- **Resource Usage**: Monitor CPU and GPU usage for complex sensor simulations
- **Real-time Factor**: Maintain real-time simulation performance with multiple sensors
- **Data Throughput**: Ensure sensor data can be processed at required rates

## Summary

Sensor simulation is fundamental to the digital twin concept for humanoid robots, enabling comprehensive testing of perception, navigation, and interaction algorithms. By accurately simulating LiDAR, depth cameras, and IMUs, researchers can develop and validate robotic systems in a safe, controlled, and cost-effective environment before deploying to real hardware.

## Key Takeaways

- Sensor simulation enables safe and repeatable testing of robotic algorithms
- LiDAR, depth cameras, and IMUs each serve distinct functions in humanoid robots
- Realistic noise models are crucial for accurate simulation
- Sensor data flows into ROS 2 using standard message formats
- Perception testing in simulation accelerates development and validation