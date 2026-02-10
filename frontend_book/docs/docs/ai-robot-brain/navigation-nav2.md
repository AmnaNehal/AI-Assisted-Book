---
title: Navigation with Nav2
sidebar_label: Navigation with Nav2
description: Learning about path planning fundamentals and navigation for humanoid movement with Nav2 and the perception → planning → action loop
keywords:
  - Navigation
  - Nav2
  - Path Planning
  - Humanoid Movement
  - Perception Planning Action
---

# Navigation with Nav2

## Overview

Navigation with Nav2 represents the culmination of the AI-robot brain concept, bringing together perception, planning, and action in a cohesive system. Nav2 (Navigation 2) is the state-of-the-art navigation framework for ROS 2, providing advanced path planning and execution capabilities specifically designed for complex robotic applications. This chapter explores path planning fundamentals, humanoid-specific navigation considerations, and the complete perception → planning → action loop.

## Path Planning Fundamentals

### Understanding Path Planning

Path planning is the process of finding a valid route from a starting position to a goal position while avoiding obstacles. In robotic navigation, path planning involves:

- **Global Planning**: Computing a route through the known environment
- **Local Planning**: Executing the path while avoiding unexpected obstacles
- **Replanning**: Adjusting the route when conditions change
- **Optimization**: Finding the most efficient path based on various criteria

### Global Path Planning

Global planners operate on a complete map of the environment to find a route from start to goal:

#### A* Algorithm
- **Heuristic Search**: Uses heuristic function to guide search towards goal
- **Optimality**: Guarantees optimal path under certain conditions
- **Memory Efficiency**: Maintains open and closed lists for efficient search

#### Dijkstra's Algorithm
- **Guaranteed Optimality**: Always finds the shortest path
- **Complete Coverage**: Explores all possible paths up to goal
- **Computational Cost**: Higher than A* for large environments

#### Gradient Path Planners
- **Potential Fields**: Uses artificial forces to guide robot
- **Fast Computation**: Real-time path generation capability
- **Local Minima**: Potential for getting stuck in local minima

### Local Path Planning

Local planners focus on immediate navigation while following the global path:

#### DWA (Dynamic Window Approach)
- **Velocity Space**: Evaluates all possible velocity combinations
- **Kinematic Constraints**: Respects robot's motion limitations
- **Safety**: Prioritizes obstacle avoidance in real-time

#### Trajectory Rollout
- **Prediction**: Evaluates future trajectories
- **Scoring**: Rates trajectories based on safety and goal achievement
- **Real-time**: Fast evaluation for dynamic environments

### Nav2 Navigation Stack Architecture

Nav2 implements a flexible, layered architecture:

```
High Level
├── Navigation Actions
├── Navigation Server
├── Behavior Trees
├── Task Executors
├── Planners (Global & Local)
├── Controllers
├── Sensors (Costmap2D)
└── Robot Drivers
Low Level
```

### Costmap2D Framework

The Costmap2D framework provides the perception interface for navigation:

#### Static Layer
- **Map Data**: Static obstacles from occupancy grid map
- **Resolution**: Configurable resolution for different applications
- **Update Rate**: Can be static or updated periodically

#### Obstacle Layer
- **Sensor Fusion**: Combines data from multiple sensors
- **Temporal Filtering**: Maintains obstacle history over time
- **Clearing**: Removes obstacles that are no longer detected

#### Inflation Layer
- **Safety Margin**: Expands obstacles to create safety buffer
- **Cost Function**: Defines how costs propagate from obstacles
- **Robot Footprint**: Considers robot size and shape

## Navigation for Humanoid Movement

### Humanoid-Specific Navigation Challenges

Humanoid robots present unique challenges for navigation systems:

#### Bipedal Locomotion
- **Balance Requirements**: Must maintain balance during movement
- **Step Planning**: Requires careful footstep placement
- **Dynamic Stability**: Center of mass considerations during walking

#### Anthropomorphic Constraints
- **Height Considerations**: Head height affects perception and planning
- **Arm Positioning**: Upper body movements affect balance
- **Weight Distribution**: Non-uniform mass distribution

#### Complex Kinematics
- **Degrees of Freedom**: Many joints affecting motion planning
- **Gait Patterns**: Specific walking patterns for stability
- **Transition States**: Standing, walking, turning, stopping

### Humanoid Navigation Strategies

#### Footstep Planning
- **Footstep Planner**: Plans where feet should be placed
- **Stability Regions**: Ensures center of mass remains stable
- **Terrain Adaptation**: Adjusts for uneven terrain

#### Whole-Body Planning
- **Center of Mass Planning**: Plans CoM trajectory for stability
- **Zero Moment Point (ZMP)**: Maintains dynamic stability
- **Joint Space Planning**: Coordinates all joint movements

#### Humanoid-Specific Controllers
- **Cart-Table (CT) Controller**: Simple inverted pendulum model
- **Linear Inverted Pendulum (LIP)**: Linearized balance control
- **Preview Control**: Uses future reference trajectory for control

### Nav2 for Humanoid Robots

Nav2 can be adapted for humanoid navigation through:

#### Custom Controllers
- **Humanoid Controller Plugins**: Specialized for bipedal motion
- **Footstep Interface**: Integration with footstep planners
- **Balance Integration**: Maintains balance during navigation

#### Specialized Parameters
- **Footprint Configuration**: Accurate robot footprint for costmaps
- **Kinematic Constraints**: Respect humanoid motion limitations
- **Balance Constraints**: Maintain stability during navigation

### Example Humanoid Navigation Configuration

```yaml
# Example Nav2 configuration for humanoid robot
bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    plugin_lib_names:
      - nav2_compute_path_to_pose_action_bt_node
      - nav2_follow_path_action_bt_node
      - nav2_back_up_action_bt_node
      - nav2_spin_action_bt_node
      - nav2_wait_action_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["HumanoidController"]

    HumanoidController:
      plugin: "nav2_mppi_controller::Controller"
      time_steps: 26
      control_freq: 20
      horizon: 1.3
      # Humanoid-specific parameters
      max_linear_speed: 0.5  # Slower for balance
      max_angular_speed: 0.6
      min_linear_speed: 0.1
      min_angular_speed: 0.1

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 6
      height: 6
      resolution: 0.05
      # Humanoid-specific footprint
      footprint: "[[-0.3, -0.2], [-0.3, 0.2], [0.4, 0.2], [0.4, -0.2]]"
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        inflation_radius: 0.55  # Larger for humanoid safety
        cost_scaling_factor: 3.0

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      footprint: "[[-0.3, -0.2], [-0.3, 0.2], [0.4, 0.2], [0.4, -0.2]]"
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
```

## Perception → Planning → Action Loop

### Understanding the Complete Loop

The perception → planning → action loop represents the complete AI-robot brain concept:

1. **Perception**: Sensors gather information about the environment
2. **Planning**: Navigation system processes perception data to make decisions
3. **Action**: Robot executes planned movements to achieve goals
4. **Feedback**: Results influence the next cycle of perception

### Perception Integration

The perception system feeds data to the navigation system:

#### Sensor Data Processing
- **Camera Data**: Object detection and semantic information
- **LiDAR Data**: Precise obstacle detection and mapping
- **IMU Data**: Robot orientation and acceleration information
- **Wheel Encoders**: Robot motion and odometry

#### Environment Understanding
- **Object Recognition**: Identifying obstacles and landmarks
- **Semantic Mapping**: Understanding environment context
- **Dynamic Object Tracking**: Following moving objects in environment
- **Scene Understanding**: Interpreting complex environmental situations

### Planning Process

The planning system processes perception data to make navigation decisions:

#### Goal Processing
- **Goal Acceptance**: Validating and accepting navigation goals
- **Goal Transformation**: Converting goals to robot coordinate frame
- **Goal Prioritization**: Managing multiple simultaneous goals

#### Path Computation
- **Global Path Planning**: Computing overall route to goal
- **Local Path Planning**: Adjusting path for immediate obstacles
- **Path Optimization**: Improving path efficiency and safety

#### Behavior Selection
- **Recovery Behaviors**: Handling navigation failures
- **Adaptive Planning**: Adjusting strategy based on conditions
- **Multi-objective Optimization**: Balancing speed, safety, and comfort

### Action Execution

The action system executes the planned navigation:

#### Motion Control
- **Velocity Commands**: Sending velocity commands to robot base
- **Trajectory Following**: Following pre-computed trajectories
- **Feedback Control**: Adjusting based on robot performance

#### Humanoid-Specific Execution
- **Gait Generation**: Creating walking patterns for stability
- **Balance Control**: Maintaining balance during movement
- **Step Execution**: Executing individual steps safely

### Integration Example

Here's how the complete loop might be implemented:

```python
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan, Image
from vision_msgs.msg import Detection2DArray
from action_msgs.msg import GoalStatus
import numpy as np

class PerceptionPlanningActionNode(Node):
    def __init__(self):
        super().__init__('perception_planning_action_node')

        # Navigation client
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Perception subscribers
        self.laser_sub = self.create_subscription(
            LaserScan, '/scan', self.laser_callback, 10)
        self.camera_sub = self.create_subscription(
            Image, '/camera/rgb/image_rect_color', self.camera_callback, 10)
        self.detection_sub = self.create_subscription(
            Detection2DArray, '/isaac_ros/detections', self.detection_callback, 10)

        # Navigation status subscription
        self.nav_status_sub = self.create_subscription(
            GoalStatus, '/navigate_to_pose/_action/status',
            self.navigation_status_callback, 10)

        # Timer for the perception-planning-action loop
        self.loop_timer = self.create_timer(0.1, self.perception_planning_action_loop)

        # State variables
        self.perception_data = {
            'obstacles': [],
            'detections': [],
            'environment': {}
        }
        self.current_goal = None
        self.navigation_active = False

    def laser_callback(self, msg):
        """Process laser scan data for obstacle detection"""
        # Process laser data to detect obstacles
        ranges = np.array(msg.ranges)
        valid_ranges = ranges[np.isfinite(ranges)]

        # Detect obstacles within robot's safety radius
        obstacle_angles = np.where(valid_ranges < 1.0)[0]  # Objects within 1m
        obstacle_distances = valid_ranges[obstacle_angles]

        self.perception_data['obstacles'] = list(zip(obstacle_angles, obstacle_distances))

    def camera_callback(self, msg):
        """Process camera data for environmental understanding"""
        # Convert and process camera data
        # This could include semantic segmentation or scene understanding
        pass

    def detection_callback(self, msg):
        """Process object detection results"""
        detections = []
        for detection in msg.detections:
            # Process each detection for navigation relevance
            if detection.results[0].hypothesis.class_id == 'person':
                detections.append({
                    'type': 'person',
                    'confidence': detection.results[0].hypothesis.score,
                    'bbox': detection.bbox
                })
        self.perception_data['detections'] = detections

    def navigation_status_callback(self, msg):
        """Monitor navigation status"""
        if msg.status_list:
            status = msg.status_list[0].status
            if status == GoalStatus.STATUS_SUCCEEDED:
                self.navigation_active = False
                self.get_logger().info('Navigation goal reached successfully')
            elif status in [GoalStatus.STATUS_ABORTED, GoalStatus.STATUS_CANCELED]:
                self.navigation_active = False
                self.get_logger().info('Navigation goal failed')

    def perception_planning_action_loop(self):
        """Main perception-planning-action loop"""
        # 1. PERCEPTION: Process all sensor data
        self.process_environment()

        # 2. PLANNING: Make navigation decisions based on perception
        action = self.decide_navigation_action()

        # 3. ACTION: Execute the planned action
        self.execute_navigation_action(action)

    def process_environment(self):
        """Process all perception data to understand environment"""
        # Update environment model based on perception data
        # This might include updating costmaps, detecting dynamic obstacles, etc.
        pass

    def decide_navigation_action(self):
        """Make navigation decisions based on perception data"""
        if not self.navigation_active:
            # If no navigation active, check if we should pursue a new goal
            if self.should_pursue_new_goal():
                return 'request_navigation'
        else:
            # If navigation is active, check for replanning needs
            if self.needs_replanning():
                return 'replan_path'
            elif self.detects_critical_obstacle():
                return 'stop_and_replan'

        return 'continue_navigation'

    def execute_navigation_action(self, action):
        """Execute the decided navigation action"""
        if action == 'request_navigation' and self.current_goal:
            self.send_navigation_goal(self.current_goal)
        elif action == 'replan_path':
            # Request replanning through Nav2
            pass
        elif action == 'stop_and_replan':
            # Emergency stop and replanning
            self.stop_navigation()
        # 'continue_navigation' requires no special action, just continue

    def should_pursue_new_goal(self):
        """Determine if we should pursue a new navigation goal"""
        # Check if we have meaningful goals to pursue
        # This could be based on detections, user commands, etc.
        return self.current_goal is not None and not self.navigation_active

    def needs_replanning(self):
        """Determine if current path needs replanning"""
        # Check for changes in environment that affect current path
        return len(self.perception_data['obstacles']) > 0

    def detects_critical_obstacle(self):
        """Check for obstacles requiring immediate action"""
        # Check for obstacles in immediate path that require stopping
        critical_obstacles = [
            obs for obs in self.perception_data['obstacles']
            if obs[1] < 0.5  # Within 0.5m
        ]
        return len(critical_obstacles) > 0

    def send_navigation_goal(self, goal_pose):
        """Send navigation goal to Nav2"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.nav_client.wait_for_server()
        future = self.nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)
        self.navigation_active = True

    def feedback_callback(self, feedback_msg):
        """Handle navigation feedback"""
        self.get_logger().info(f'Navigation progress: {feedback_msg.current.pose}')

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.navigation_active = False
            return

        self.get_logger().info('Goal accepted')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle navigation result"""
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result}')
        self.navigation_active = False

def main(args=None):
    rclpy.init(args=args)
    pp_action_node = PerceptionPlanningActionNode()

    try:
        rclpy.spin(pp_action_node)
    except KeyboardInterrupt:
        pass
    finally:
        pp_action_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Advanced Navigation Concepts

### Multi-Robot Navigation

Nav2 supports multi-robot scenarios:

#### Coordination Strategies
- **Centralized Coordination**: Central controller manages all robots
- **Decentralized Coordination**: Robots coordinate among themselves
- **Hybrid Approaches**: Combination of centralized and decentralized

#### Collision Avoidance
- **Communication-Based**: Robots share position and intentions
- **Reservation-Based**: Reserving space and time for movements
- **Rule-Based**: Following navigation rules (e.g., right-hand traffic)

### Dynamic Environment Navigation

Handling environments with moving obstacles:

#### Prediction Models
- **Constant Velocity**: Assuming obstacles maintain current velocity
- **Social Force**: Modeling social interactions and behaviors
- **Learning-Based**: Using machine learning for prediction

#### Reactive Strategies
- **Local Replanning**: Quick replanning when obstacles appear
- **Velocity Obstacles**: Computing safe velocities to avoid collisions
- **Time-Parameterized Paths**: Planning paths that account for time

## Integration with Isaac ROS Perception

### Perception-Navigation Integration

The integration between Isaac ROS perception and Nav2 navigation:

#### Sensor Data Flow
- **Isaac ROS Perception** → **Nav2 Costmaps** → **Path Planning** → **Execution**

#### Data Formats
- **Sensor Messages**: ROS 2 standard formats (sensor_msgs)
- **Perception Results**: vision_msgs for object detection and tracking
- **Map Updates**: nav_msgs for occupancy grid updates

### Example Integration Pipeline

```yaml
# Complete perception-to-navigation pipeline
perception_to_navigation:
  # Isaac ROS perception pipeline
  image_rectification:
    package: "isaac_ros_image_proc"
    executable: "rectify_node"

  object_detection:
    package: "isaac_ros_detectnet"
    executable: "detectnet"

  visual_slam:
    package: "isaac_ros_visual_slam"
    executable: "visual_slam_node"

  # Nav2 navigation stack
  costmap_obstacle_layer:
    # Receives sensor data from Isaac ROS
    input_topics: ["/camera/depth/image_rect", "/scan"]

  global_planner:
    # Uses map and SLAM pose for path planning

  local_planner:
    # Uses local costmap for obstacle avoidance

  controller:
    # Executes velocity commands for robot
```

## Best Practices for Navigation Implementation

### System Design
- **Modular Architecture**: Separate perception, planning, and control components
- **Parameter Management**: Use ROS 2 parameters for easy configuration
- **Error Handling**: Implement robust error recovery mechanisms

### Performance Optimization
- **Computational Efficiency**: Optimize algorithms for real-time performance
- **Memory Management**: Efficiently manage memory for perception and mapping
- **Communication Optimization**: Minimize message overhead between nodes

### Safety Considerations
- **Fail-Safe Mechanisms**: Implement safe stopping procedures
- **Validation**: Verify path feasibility before execution
- **Monitoring**: Continuously monitor navigation performance

## Summary

Navigation with Nav2 completes the AI-robot brain concept by connecting perception systems to action execution. Through path planning fundamentals, humanoid-specific navigation considerations, and the perception → planning → action loop, Nav2 enables robots to autonomously navigate complex environments. The integration with Isaac ROS perception systems provides a complete pipeline for intelligent robot navigation, demonstrating how perception, planning, and action work together to create intelligent robotic behavior.

## Key Takeaways

- Nav2 provides comprehensive navigation capabilities for complex robots
- Humanoid navigation requires special consideration for bipedal locomotion
- The perception → planning → action loop forms the complete AI-robot brain
- Integration between perception and navigation systems is crucial
- Best practices ensure safe and efficient navigation implementation