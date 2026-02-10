# Data Model: AI-Robot Brain (NVIDIA Isaac™)

**Feature**: Module 3 – The AI-Robot Brain (NVIDIA Isaac™)
**Date**: 2025-12-18
**Model Type**: Content and Configuration Data Model
**Previous Stage**: research.md → **Next Stage**: contracts/

## Overview

This data model defines the content structure, configuration elements, and data relationships for the AI-Robot Brain educational module. It encompasses educational content, simulation configurations, and documentation assets that will be delivered through the Docusaurus platform.

## Content Data Structure

### Chapter-Level Entities

#### AI Robot Brain Chapter
- **chapterId**: String (unique identifier: "nvidia-isaac-sim", "isaac-ros-perception", "navigation-nav2")
- **title**: String (display title for the chapter)
- **description**: String (brief overview of chapter content)
- **learningObjectives**: Array<String> (specific learning outcomes)
- **prerequisites**: Array<String> (required knowledge areas)
- **duration**: Number (estimated completion time in minutes)
- **difficultyLevel**: Enum ("beginner", "intermediate", "advanced")
- **relatedTopics**: Array<String> (cross-references to other content)
- **assets**: Array<AI Robot BrainAsset> (diagrams, images, examples for the chapter)

### Content Elements

#### AI Robot Brain Concept
- **conceptId**: String (unique identifier)
- **name**: String (concept name)
- **definition**: String (detailed explanation)
- **examples**: Array<String> (practical examples)
- **visualRepresentations**: Array<AI Robot BrainAsset> (diagrams, charts, illustrations)
- **category**: Enum ("simulation", "perception", "navigation", "integration")
- **complexityScore**: Number (1-5 scale indicating difficulty)
- **dependencies**: Array<String> (other concepts this builds upon)

#### AI Robot Brain Asset
- **assetId**: String (unique identifier)
- **title**: String (descriptive title)
- **type**: Enum ("diagram", "image", "video", "interactive", "simulation-config")
- **filePath**: String (relative path from static directory)
- **altText**: String (accessibility description)
- **caption**: String (educational caption)
- **chapterId**: String (which chapter this asset belongs to)
- **contentType**: Enum ("explanatory", "demonstrative", "comparative", "tutorial")

## Configuration Data

### Docusaurus Site Configuration
- **siteConfig**: Object containing:
  - **title**: String ("AI-Robot Brain Education")
  - **tagline**: String ("Learning NVIDIA Isaac for Humanoid Robot Perception, Navigation, and Training")
  - **url**: String (deployment URL)
  - **baseUrl**: String (base path for deployment)
  - **organizationName**: String (GitHub organization)
  - **projectName**: String (repository name)
  - **trailingSlash**: Boolean (URL structure preference)
  - **favicon**: String (path to favicon)
  - **themes**: Array<String> (active Docusaurus themes)
  - **presets**: Array<Object> (Docusaurus preset configurations)

### Navigation Structure
- **sidebarConfig**: Object containing:
  - **aiRobotBrainSidebar**: Array<SidebarItem>
  - **sidebarLabel**: String ("AI-Robot Brain Module")
  - **position**: Number (navigation position)
  - **collapsible**: Boolean (whether sidebar can collapse)

#### SidebarItem
- **type**: String ("doc", "category", "link")
- **id**: String (reference to document)
- **label**: String (display text)
- **className**: String (CSS classes)
- **customProps**: Object (additional properties)
- **items**: Array<SidebarItem> (nested items for category type)

## Simulation Configuration Data

### Isaac Sim Configuration
- **isaacSimConfig**: Object containing:
  - **worldFile**: String (path to Isaac Sim world definition)
  - **renderer**: String ("ogre2", "optix", "embree")
  - **realTimeFactor**: Number (simulation speed multiplier)
  - **physicsEngine**: String ("PhysX", "Bullet")
  - **robotModels**: Array<RobotModelConfig>
  - **sensorConfigs**: Array<SensorConfig>

#### RobotModelConfig
- **modelName**: String (unique model identifier)
- **usdPath**: String (path to USD robot description)
- **initialPose**: Object {x, y, z, roll, pitch, yaw}
- **plugins**: Array<String> (Isaac Sim plugins to load)
- **materials**: Array<MaterialConfig> (visual properties)

#### MaterialConfig
- **materialName**: String (identifier)
- **color**: String (hex color code)
- **texture**: String (optional texture path)
- **roughness**: Number (material roughness property)
- **metallic**: Number (material metallic property)

#### SensorConfig
- **sensorType**: String ("camera", "lidar", "imu", "depth_camera", "radar")
- **sensorName**: String (unique identifier)
- **topicName**: String (ROS 2 topic for data publishing)
- **updateRate**: Number (frequency of sensor updates)
- **mountingPose**: Object {x, y, z, roll, pitch, yaw}
- **sensorParameters**: Object (type-specific parameters)

### Isaac ROS Perception Configuration
- **isaacROSConfig**: Object containing:
  - **perceptionPipeline**: String (name of perception pipeline)
  - **accelerationType**: String ("CUDA", "TensorRT", "CPU")
  - **inputTopics**: Array<String> (topics for sensor input)
  - **outputTopics**: Array<String> (topics for processed output)
  - **processingModules**: Array<PerceptionModule>

#### PerceptionModule
- **moduleName**: String (name of perception module)
- **moduleType**: String ("object_detection", "segmentation", "slam", "tracking")
- **inputFormat**: String (expected input format)
- **outputFormat**: String (output format produced)
- **acceleration**: String ("CUDA", "TensorRT", "CPU")

## Educational Assessment Data

### Learning Objective Assessment
- **assessmentConfig**: Object containing:
  - **knowledgeChecks**: Array<KnowledgeCheck>
  - **practicalExercises**: Array<PracticalExercise>
  - **completionCriteria**: Array<CompletionCriterion>

#### KnowledgeCheck
- **checkId**: String (unique identifier)
- **question**: String (assessment question)
- **answerOptions**: Array<AnswerOption>
- **correctAnswer**: String (identifier of correct option)
- **explanation**: String (rationale for correct answer)
- **difficulty**: Enum ("easy", "medium", "hard")

#### AnswerOption
- **optionId**: String (unique identifier)
- **text**: String (answer text)
- **isCorrect**: Boolean (whether this is the correct answer)

#### PracticalExercise
- **exerciseId**: String (unique identifier)
- **title**: String (exercise name)
- **instructions**: String (step-by-step guide)
- **expectedOutcome**: String (what students should achieve)
- **verificationSteps**: Array<String> (how to confirm completion)
- **resources**: Array<String> (required files/tools)

#### CompletionCriterion
- **criterionId**: String (unique identifier)
- **description**: String (what constitutes completion)
- **weight**: Number (importance in overall assessment)
- **method**: Enum ("quiz", "practical", "portfolio")

## Relationships and Constraints

### Content Hierarchy
- AI Robot Brain Chapter 1--* AI Robot Brain Concept
- AI Robot Brain Chapter 1--* AI Robot Brain Asset
- AI Robot Brain Concept 1--* AI Robot Brain Asset (visual representations)

### Configuration Dependencies
- Docusaurus Site Configuration → Navigation Structure
- Isaac Sim Configuration → RobotModelConfig
- Isaac ROS Configuration → PerceptionModule
- Learning Objective Assessment → AI Robot Brain Chapter

### Validation Rules
- Each chapter must have 3-7 learning objectives
- Each concept must belong to exactly one category
- Asset file paths must exist in the static directory
- Simulation configurations must be syntactically valid
- Assessment questions must have exactly one correct answer

## Performance Considerations

### Content Loading
- Assets should be optimized for fast loading (<500KB per image)
- Videos should be compressed with appropriate quality settings
- Interactive elements should have fallback static content
- Progressive loading for large diagrams

### Search and Indexing
- All content should be searchable via Docusaurus search
- Metadata should be rich enough for semantic search
- Cross-references should be maintained for related content
- Breadcrumb navigation should reflect content hierarchy

## Extensibility Points

### New Chapter Addition
- New AI Robot Brain Chapter entities can be added to extend curriculum
- Related AI Robot Brain Concept and AI Robot Brain Asset entities can be linked
- Existing assessment structures can be reused or extended

### Advanced Topic Integration
- Advanced AI Robot Brain Concept entities can be added to existing categories
- New AI Robot Brain Asset types can be introduced for specialized content
- Assessment structures can accommodate new evaluation methods

## Data Integrity

### Consistency Checks
- All referenced assets must exist in the file system
- Cross-chapter references must resolve to valid content
- Configuration values must be within acceptable ranges
- Learning objectives must align with chapter content

### Backup and Recovery
- Content should be version-controlled in Git
- Configuration should be documented and reproducible
- Assets should be stored in the repository or reliable CDN
- Regular validation of content integrity should be performed