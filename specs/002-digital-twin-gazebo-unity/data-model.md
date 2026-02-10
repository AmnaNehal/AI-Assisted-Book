# Data Model: Digital Twin (Gazebo & Unity)

**Feature**: Module 2 – The Digital Twin (Gazebo & Unity)
**Date**: 2025-12-18
**Model Type**: Content and Configuration Data Model
**Previous Stage**: research.md → **Next Stage**: contracts/

## Overview

This data model defines the content structure, configuration elements, and data relationships for the Digital Twin educational module. It encompasses educational content, simulation configurations, and documentation assets that will be delivered through the Docusaurus platform.

## Content Data Structure

### Chapter-Level Entities

#### DigitalTwinChapter
- **chapterId**: String (unique identifier: "physics-simulation", "unity-environments", "sensor-simulation")
- **title**: String (display title for the chapter)
- **description**: String (brief overview of chapter content)
- **learningObjectives**: Array<String> (specific learning outcomes)
- **prerequisites**: Array<String> (required knowledge areas)
- **duration**: Number (estimated completion time in minutes)
- **difficultyLevel**: Enum ("beginner", "intermediate", "advanced")
- **relatedTopics**: Array<String> (cross-references to other content)
- **assets**: Array<DigitalTwinAsset> (diagrams, images, examples for the chapter)

### Content Elements

#### DigitalTwinConcept
- **conceptId**: String (unique identifier)
- **name**: String (concept name)
- **definition**: String (detailed explanation)
- **examples**: Array<String> (practical examples)
- **visualRepresentations**: Array<DigitalTwinAsset> (diagrams, charts, illustrations)
- **category**: Enum ("physics", "visualization", "sensors", "integration")
- **complexityScore**: Number (1-5 scale indicating difficulty)
- **dependencies**: Array<String> (other concepts this builds upon)

#### DigitalTwinAsset
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
  - **title**: String ("Digital Twin Education")
  - **tagline**: String ("Learning Gazebo, Unity, and ROS 2 Integration")
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
  - **digitalTwinSidebar**: Array<SidebarItem>
  - **sidebarLabel**: String ("Digital Twin Module")
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

### Gazebo Simulation Config
- **gazeboConfig**: Object containing:
  - **worldFile**: String (path to Gazebo world definition)
  - **physicsEngine**: String ("ode", "bullet", "dart")
  - **gravity**: Array<Number> (x, y, z gravity vector)
  - **realTimeFactor**: Number (simulation speed multiplier)
  - **maxStepSize**: Number (maximum physics step size)
  - **robotModels**: Array<RobotModelConfig>
  - **sensorConfigs**: Array<SensorConfig>

#### RobotModelConfig
- **modelName**: String (unique model identifier)
- **urdfPath**: String (path to URDF description)
- **initialPose**: Object {x, y, z, roll, pitch, yaw}
- **plugins**: Array<String> (Gazebo plugins to load)
- **materials**: Array<MaterialConfig> (visual properties)

#### MaterialConfig
- **materialName**: String (identifier)
- **color**: String (hex color code)
- **texture**: String (optional texture path)
- **shininess**: Number (specular reflection property)

#### SensorConfig
- **sensorType**: String ("lidar", "camera", "imu", "depth_camera")
- **sensorName**: String (unique identifier)
- **topicName**: String (ROS 2 topic for data publishing)
- **updateRate**: Number (frequency of sensor updates)
- **mountingPose**: Object {x, y, z, roll, pitch, yaw}
- **sensorParameters**: Object (type-specific parameters)

### Unity Scene Configuration
- **unitySceneConfig**: Object containing:
  - **sceneName**: String (Unity scene identifier)
  - **environmentSettings**: EnvironmentConfig
  - **lightingConfig**: LightingConfig
  - **robotPrefab**: String (path to robot model prefab)
  - **interactionElements**: Array<InteractionElement>

#### EnvironmentConfig
- **skybox**: String (path to skybox material)
- **fogEnabled**: Boolean (atmospheric fog)
- **fogDensity**: Number (fog intensity)
- **terrainSettings**: TerrainConfig

#### TerrainConfig
- **terrainType**: String ("indoor", "outdoor", "custom")
- **collisionMesh**: String (path to collision geometry)
- **textures**: Array<TextureLayer>

#### TextureLayer
- **texturePath**: String (albedo texture)
- **normalMapPath**: String (normal map)
- **tileSize**: Number (texture repetition scale)

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
- DigitalTwinChapter 1--* DigitalTwinConcept
- DigitalTwinChapter 1--* DigitalTwinAsset
- DigitalTwinConcept 1--* DigitalTwinAsset (visual representations)

### Configuration Dependencies
- Docusaurus Site Configuration → Navigation Structure
- Gazebo Simulation Config → RobotModelConfig
- Unity Scene Configuration → EnvironmentConfig
- Learning Objective Assessment → DigitalTwinChapter

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
- New DigitalTwinChapter entities can be added to extend curriculum
- Related DigitalTwinConcept and DigitalTwinAsset entities can be linked
- Existing assessment structures can be reused or extended

### Advanced Topic Integration
- Advanced DigitalTwinConcept entities can be added to existing categories
- New DigitalTwinAsset types can be introduced for specialized content
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