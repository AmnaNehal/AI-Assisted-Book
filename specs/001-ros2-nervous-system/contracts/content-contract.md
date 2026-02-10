# Content Contract: ROS 2 Nervous System Module

## Overview
This contract defines the structure, metadata, and validation rules for the ROS 2 Nervous System educational content.

## Content Structure Contract

### Required Frontmatter
Each chapter file MUST include the following frontmatter:

```yaml
---
title: <Chapter Title>
sidebar_position: <number>
description: <Brief description>
tags: [ros2, robotics, ai]
---
```

### Required Sections
Each chapter file MUST contain the following sections:
- Learning Objectives
- Main Content (organized by specification requirements)
- Summary/Key Takeaways
- References/Further Reading (if applicable)

## Navigation Contract

### Sidebar Structure
The sidebar MUST be organized as:
```
ROS 2 Nervous System
├── Fundamentals
├── Python Agents to ROS 2
└── Humanoid Modeling with URDF
```

### Navigation Properties
- All chapters MUST be accessible via sidebar navigation
- Chapters MUST be ordered according to priority (P1, P2, P3) from specification
- Each chapter link MUST display the proper title as defined in the frontmatter

## Content Validation Contract

### Format Requirements
- All content MUST be in Docusaurus-compatible Markdown format (FR-008)
- Code examples MUST be minimal and serve educational purpose only (FR-009)
- Diagrams and visual aids MUST be clear and support learning objectives (FR-010)

### Educational Requirements
- Content MUST explain ROS 2 as middleware for AI agents and robot controllers (FR-001)
- Communication primitives (nodes, topics, services) MUST be explained (FR-002)
- Python AI agent connection via rclpy MUST be covered (FR-003)
- AI decision → ROS command → robot action flow MUST be described (FR-004)
- URDF purpose and structure MUST be explained (FR-005)
- Links, joints, and kinematics concepts MUST be covered (FR-006)
- URDF's role in simulation and control MUST be explained (FR-007)

## Quality Assurance Contract

### Success Criteria Validation
Each chapter MUST contribute to meeting the following success criteria:
- SC-001: Students understand ROS 2 as robotic nervous system (covered in Fundamentals)
- SC-002: Students explain communication primitives (covered in Fundamentals)
- SC-003: Students understand AI-ROS integration via URDF (covered in Python Agents and URDF Modeling)
- SC-004: Students describe AI decision flow (covered in Python Agents)
- SC-005: Student satisfaction with module (measured after completion)

## Technical Contract

### File Structure
```
docs/
├── docs/
│   └── ros2-nervous-system/
│       ├── fundamentals.md
│       ├── python-agents.md
│       └── urdf-modeling.md
├── static/
│   └── img/
└── sidebars.js
```

### Build Requirements
- Site MUST build successfully using `npm run build`
- All internal links MUST resolve correctly
- All images MUST load without errors
- Navigation MUST work across all supported browsers