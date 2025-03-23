# System Patterns for RovVision2_Sonar

## System Architecture

### Distributed System Architecture
The system follows a distributed architecture with two primary components:
1. **Ground Control Station**: Human interface running on a surface computer
2. **Onboard System**: Software running on the ROV's computer

### Communication Architecture
- **ZMQ Messaging**: Core communication protocol using publisher/subscriber pattern
- **UDP Transmission**: Used for real-time video and sonar image transmission
- **Topic-based Messaging**: Structured around distinct message topics (`zmq_topics.py`)

### Data Flow
```
[Sensors] → [Sensor Gates] → [ZMQ Network] → [Ground Control] → [User Interface]
                                   ↑
[Cameras] → [Image Gate] →  [UDP Network] 
                                   ↑
[Sonars]  → [Sonar Gate] →  [UDP Network]
```

## Key Design Patterns

### Publisher-Subscriber Pattern
- ZMQ-based pub/sub system for distributing telemetry, commands, and state information
- Decouples data producers from consumers
- Allows multiple subscribers to receive the same data

### Gateway Pattern
- Specialized "gates" for each data type (imGate.py, sonGate.py, udpGate.py, etc.)
- Handles data acquisition, preprocessing, and distribution
- Isolates device-specific code from the rest of the system

### Model-View-Controller (MVC)
- **Model**: State management in the controller and sensors
- **View**: Ground control UI (rovViewer.py)
- **Controller**: Command processing and control logic

### Command Pattern
- Structured command objects for ROV control
- Allows for recording, playback, and automated command sequences

### Observer Pattern
- UI components observe system state changes
- Updates triggered by ZMQ message arrivals

## Technical Implementation

### Threading Model
- Asynchronous event handling using background threads
- Main UI thread for user interaction
- Background threads for network communication

### Image Processing Pipeline
1. Image acquisition from cameras
2. Optional preprocessing (resize, compression)
3. UDP transmission to ground control
4. Decompression and display on UI

### Control Systems
- PID controllers for:
  - Depth holding
  - Attitude (roll, pitch, yaw) stabilization
  - Position holding

### Configuration Management
- Central configuration in `config.py`
- Support for multiple ROV configurations through environment variables
- Runtime-configurable parameters

## Key Technical Decisions

### UDP for Video Transmission
- Lower latency than TCP for real-time video
- Acceptable packet loss in exchange for reduced latency
- Compression to manage bandwidth limitations

### ZMQ for Command and Telemetry
- Reliable messaging system with pub/sub capabilities
- Built-in support for multiple transport protocols
- Good performance characteristics for small messages

### Python as Primary Language
- Rapid development capabilities
- Rich ecosystem for scientific computing and computer vision
- Cross-platform compatibility

### Tkinter for UI
- Built-in UI toolkit with Python
- Lightweight and reliable
- Suitable for creating technical interfaces

### OpenCV for Image Processing
- Industry-standard computer vision library
- Extensive capabilities for image manipulation and analysis
- Good performance characteristics 