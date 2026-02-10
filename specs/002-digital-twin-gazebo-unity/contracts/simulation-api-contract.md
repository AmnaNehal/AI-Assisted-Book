# API Contract: Digital Twin Simulation Interface

**Feature**: Module 2 – The Digital Twin (Gazebo & Unity)
**Contract Type**: Educational API Interface Specification
**Date**: 2025-12-18
**Version**: 1.0.0
**Previous Stage**: quickstart.md → **Next Stage**: tasks.md

## Overview

This contract defines the interface specifications for the digital twin simulation components that students will interact with during the educational module. It covers the APIs, data formats, and communication protocols used in Gazebo, Unity, and ROS 2 integration.

## Gazebo Simulation API Contract

### World Control Interface
```
POST /world/{world_name}/reset
Content-Type: application/json
Authorization: Bearer {simulation_token}

Request Body:
{
  "reset_type": "full" | "time_only" | "model_poses",
  "options": {
    "preserve_models": ["robot1", "robot2"],
    "reset_time": true
  }
}

Response: 200 OK
{
  "status": "success",
  "timestamp": "2025-12-18T10:30:00Z",
  "world_state": "reset"
}
```

### Model Spawn Interface
```
POST /model/spawn
Content-Type: application/xml
Authorization: Bearer {simulation_token}

Request Body: (URDF or SDF model definition)

Response: 201 Created
{
  "model_name": "humanoid_robot",
  "model_id": "robot_001",
  "spawn_position": {"x": 0, "y": 0, "z": 1},
  "status": "spawned"
}
```

### Sensor Data Interface
```
GET /sensor/{sensor_name}/data
Accept: application/json

Response: 200 OK
{
  "sensor_name": "lidar_360",
  "timestamp": "2025-12-18T10:30:00.123Z",
  "data": {
    "ranges": [0.1, 0.2, 0.3, ...],
    "intensities": [100, 95, 90, ...],
    "angle_min": -3.14,
    "angle_max": 3.14,
    "angle_increment": 0.01
  }
}
```

## ROS 2 Communication Contract

### Topic Definitions

#### /sensor_scan (sensor_msgs/LaserScan)
```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
```

#### /imu_data (sensor_msgs/Imu)
```
std_msgs/Header header
geometry_msgs/Quaternion orientation
float64[9] orientation_covariance
geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance
geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance
```

#### /joint_states (sensor_msgs/JointState)
```
std_msgs/Header header
string[] name
float64[] position
float64[] velocity
float64[] effort
```

## Unity-ROS Bridge Contract

### TCP Communication Protocol
```
Message Format:
{
  "op": "publish" | "subscribe" | "service_request",
  "topic": "/sensor_data",
  "type": "sensor_msgs/LaserScan",
  "msg": { /* message payload */ },
  "id": "unique_message_id",
  "fragment_size": 0,
  "compression": "none"
}
```

### Service Interface
```
GET /unity-ros/bridge/status
Response: 200 OK
{
  "bridge_status": "connected",
  "ros_master_uri": "http://localhost:11311",
  "connection_time": "2025-12-18T10:30:00Z",
  "topics": ["/sensor_data", "/robot_control", "/unity_visualization"],
  "services": ["/reset_simulation", "/spawn_robot"]
}
```

## Data Format Specifications

### Simulation Configuration Format
```json
{
  "simulation": {
    "name": "digital_twin_demo",
    "version": "1.0",
    "physics": {
      "engine": "ode",
      "gravity": [0, 0, -9.81],
      "real_time_factor": 1.0,
      "max_step_size": 0.001
    },
    "environment": {
      "world_file": "digital_twin_world.sdf",
      "lighting": "default",
      "collision_meshes": true
    },
    "robots": [
      {
        "model": "humanoid.urdf",
        "spawn_pose": {"x": 0, "y": 0, "z": 1, "roll": 0, "pitch": 0, "yaw": 0},
        "sensors": ["lidar", "imu", "camera"]
      }
    ]
  }
}
```

### Sensor Calibration Format
```json
{
  "sensor_calibrations": {
    "lidar_360": {
      "type": "ray",
      "fov": 360,
      "resolution": 0.5,
      "range_min": 0.1,
      "range_max": 10.0,
      "noise_model": "gaussian",
      "noise_stddev": 0.01
    },
    "imu_sensor": {
      "type": "imu",
      "accelerometer_noise_density": 0.017,
      "gyroscope_noise_density": 0.0006,
      "update_rate": 100
    }
  }
}
```

## Error Handling Contract

### Standard Error Response
```json
{
  "error": {
    "code": "SIMULATION_ERROR" | "CONNECTION_ERROR" | "VALIDATION_ERROR",
    "message": "Descriptive error message",
    "details": "Additional error details",
    "timestamp": "2025-12-18T10:30:00Z",
    "request_id": "unique_request_identifier"
  }
}
```

### Common Error Codes
- `SIMULATION_ERROR`: Issues with simulation execution
- `CONNECTION_ERROR`: Network or communication failures
- `VALIDATION_ERROR`: Invalid input data format
- `RESOURCE_UNAVAILABLE`: Required resources not accessible
- `PERMISSION_DENIED`: Insufficient access rights

## Performance Guarantees

### Response Time SLAs
- Sensor data queries: <50ms p95
- Simulation control commands: <100ms p95
- Model spawn operations: <200ms p95
- World reset operations: <500ms p95

### Throughput Requirements
- Minimum 60 sensor data updates per second
- Support for 10+ concurrent robot models
- Handle 1MB+ message payloads for image data

## Security Considerations

### Authentication
- API tokens required for all simulation control operations
- Certificate-based authentication for production environments
- Session timeout after 30 minutes of inactivity

### Authorization
- Read-only access for student accounts
- Simulation control permissions for instructor accounts
- Administrative access for system configuration

## Compatibility Guarantees

### Versioning Strategy
- Semantic versioning (MAJOR.MINOR.PATCH)
- Backward compatibility maintained for 2 major versions
- Deprecation notice provided 3 months before removal

### Supported Versions
- ROS 2: Humble Hawksbill (LTS)
- Gazebo: Harmonic and Garden
- Unity: 2022.3 LTS and newer
- Node.js: v18+ for documentation