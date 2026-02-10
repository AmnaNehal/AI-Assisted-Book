# API Contract: Isaac AI-Robot Brain Interface

**Feature**: Module 3 – The AI-Robot Brain (NVIDIA Isaac™)
**Contract Type**: Educational API Interface Specification
**Date**: 2025-12-18
**Version**: 1.0.0
**Previous Stage**: quickstart.md → **Next Stage**: tasks.md

## Overview

This contract defines the interface specifications for the Isaac AI-robot brain components that students will interact with during the educational module. It covers the APIs, data formats, and communication protocols used in Isaac Sim, Isaac ROS, and Nav2 integration.

## Isaac Sim API Contract

### Simulation Control Interface
```
POST /simulation/{simulation_name}/control
Content-Type: application/json
Authorization: Bearer {simulation_token}

Request Body:
{
  "command": "start" | "stop" | "reset" | "pause",
  "options": {
    "real_time_factor": 1.0,
    "physics_only": false
  }
}

Response: 200 OK
{
  "status": "success",
  "timestamp": "2025-12-18T10:30:00Z",
  "simulation_state": "running"
}
```

### Asset Management Interface
```
POST /assets/load
Content-Type: application/usd
Authorization: Bearer {simulation_token}

Request Body: (USD file content)

Response: 201 Created
{
  "asset_name": "humanoid_robot",
  "asset_id": "robot_001",
  "load_position": {"x": 0, "y": 0, "z": 1},
  "status": "loaded"
}
```

### Sensor Data Interface
```
GET /sensors/{sensor_name}/data
Accept: application/json

Response: 200 OK
{
  "sensor_name": "isaac_camera",
  "timestamp": "2025-12-18T10:30:00.123Z",
  "data": {
    "image": {"width": 1920, "height": 1080, "encoding": "rgb8"},
    "camera_info": {
      "K": [fx, 0, cx, 0, fy, cy, 0, 0, 1],
      "D": [k1, k2, p1, p2, k3],
      "resolution": [1920, 1080]
    }
  }
}
```

## Isaac ROS Communication Contract

### Perception Pipeline Topics

#### /isaac_ros/detections (detectnet_msgs/Detections2D)
```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
detectnet_msgs/ObjectArray detections
  detectnet_msgs/Detection[] detections
    int64 id
    string label
    float64 confidence
    sensor_msgs/RegionOfInterest bbox
```

#### /isaac_ros/pointcloud (sensor_msgs/PointCloud2)
```
std_msgs/Header header
sensor_msgs/PointField[] fields
bool is_bigendian
uint32 point_step
uint32 row_step
uint8[] data
bool is_dense
```

#### /isaac_ros/visual_slam/pose_graph (geometry_msgs/PoseWithCovarianceStamped)
```
std_msgs/Header header
geometry_msgs/PoseWithCovariance pose
```

## Nav2 Communication Contract

### Navigation Action Interface
```
Action: /navigate_to_pose
Action Interface: nav2_msgs/NavigateToPose

Goal:
{
  "pose": {
    "header": {"frame_id": "map"},
    "pose": {
      "position": {"x": 1.0, "y": 2.0, "z": 0.0},
      "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}
    }
  },
  "behavior_tree": "default_nav_tree"
}

Result:
{
  "result_code": 1, // SUCCEEDED
  "message": "Goal reached successfully"
}
```

### Costmap Services
```
GET /global_costmap/clear
Response: 200 OK
{
  "status": "success",
  "message": "Global costmap cleared"
}

GET /local_costmap/clear
Response: 200 OK
{
  "status": "success",
  "message": "Local costmap cleared"
}
```

## Data Format Specifications

### Perception Configuration Format
```json
{
  "perception_pipeline": {
    "name": "isaac_humanoid_perception",
    "version": "1.0",
    "modules": [
      {
        "type": "object_detection",
        "acceleration": "CUDA",
        "model": "resnet18_detector",
        "input_topic": "/camera/rgb/image_rect_color",
        "output_topic": "/isaac_ros/detections"
      },
      {
        "type": "visual_slam",
        "acceleration": "CUDA",
        "input_topics": ["/camera/rgb/image_rect_color", "/camera/depth/image_rect"],
        "output_topics": ["/isaac_ros/visual_slam/pose", "/isaac_ros/visual_slam/map"]
      }
    ],
    "parameters": {
      "confidence_threshold": 0.5,
      "max_objects": 10,
      "tracking_enabled": true
    }
  }
}
```

### Navigation Configuration Format
```json
{
  "navigation_config": {
    "name": "humanoid_navigation",
    "version": "1.0",
    "global_planner": "navfn_planner",
    "local_planner": "dwb_controller",
    "costmap_config": {
      "global": {
        "resolution": 0.05,
        "robot_radius": 0.3,
        "inflation_radius": 0.55
      },
      "local": {
        "resolution": 0.025,
        "robot_radius": 0.3,
        "inflation_radius": 0.35
      }
    },
    "humanoid_specific": {
      "max_step_height": 0.15,
      "footprint_margin": 0.1,
      "bipedal_constraints": true
    }
  }
}
```

## Error Handling Contract

### Standard Error Response
```json
{
  "error": {
    "code": "PERCEPTION_ERROR" | "NAVIGATION_ERROR" | "SIMULATION_ERROR",
    "message": "Descriptive error message",
    "details": "Additional error details",
    "timestamp": "2025-12-18T10:30:00Z",
    "request_id": "unique_request_identifier"
  }
}
```

### Common Error Codes
- `PERCEPTION_ERROR`: Issues with perception pipeline execution
- `NAVIGATION_ERROR`: Navigation planning or execution failures
- `SIMULATION_ERROR`: Isaac Sim environment issues
- `CONNECTION_ERROR`: Network or communication failures
- `VALIDATION_ERROR`: Invalid input data format

## Performance Guarantees

### Response Time SLAs
- Perception pipeline processing: <100ms p95 (with GPU acceleration)
- Navigation goal execution: <500ms p95 for local navigation
- SLAM map updates: <200ms p95
- Simulation state changes: <50ms p95

### Throughput Requirements
- Minimum 30 FPS for perception processing with GPU acceleration
- Support for 10+ concurrent perception pipelines
- Handle 1MB+ point cloud data payloads
- Maintain real-time navigation with 10Hz update rate

## Security Considerations

### Authentication
- API tokens required for all Isaac Sim control operations
- Certificate-based authentication for production environments
- Session timeout after 30 minutes of inactivity

### Authorization
- Read-only access for student accounts
- Perception pipeline configuration for instructor accounts
- Administrative access for system configuration

## Compatibility Guarantees

### Versioning Strategy
- Semantic versioning (MAJOR.MINOR.PATCH)
- Backward compatibility maintained for 2 major versions
- Deprecation notice provided 3 months before removal

### Supported Versions
- ROS 2: Humble Hawksbill (LTS)
- Isaac Sim: 2023.1+
- Isaac ROS: 3.0+
- Nav2: Humble compatible version
- Node.js: v18+ for documentation