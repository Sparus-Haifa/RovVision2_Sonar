# Technical Context for RovVision2_Sonar

## Technology Stack

### Programming Languages
- **Python**: Primary language for both onboard and ground control systems
- **Bash**: Used for utility scripts and system configuration

### Communication Frameworks
- **ZeroMQ (ZMQ)**: Core messaging system for telemetry and commands
- **UDP**: Used for high-throughput, low-latency video streaming

### User Interface
- **Tkinter**: Main UI framework for the ground control station
- **Matplotlib**: Used for plotting sensor data and telemetry
- **PIL/Pillow**: Image handling for display purposes

### Vision Processing
- **OpenCV**: Computer vision library for image processing
- **NumPy**: Numerical processing library for array operations

### System Components
- **Docker**: Used for containerization and deployment
- **Linux**: Primary operating system for both onboard and ground systems

## Development Environment

### Setup Requirements
- Python 3.x environment
- Docker for containerized deployment 
- Required Python packages (see below)

### Key Dependencies
- `numpy`: Numerical computations and array operations
- `opencv-python`: Computer vision algorithms
- `pyzmq`: ZeroMQ messaging library
- `matplotlib`: Plotting and data visualization
- `pillow`: Image processing library
- `socket`: Network communications
- `pickle`: Object serialization
- `asyncio`: Asynchronous I/O handling

### Build and Deployment
- Docker containers used for consistent deployment
- `build.sh` script for building the containers
- `run.sh` script for launching the system

## Hardware Integration

### Camera Systems
- Support for stereo and mono camera configurations
- Multiple camera resolutions supported (configured in `config.py`)
- IDS uEye cameras (driver-specific integration)

### Sonar Integration
- Support for sonar imaging devices 
- Processing of sonar data for visualization

### Control Hardware
- Joystick input for manual control
- Support for various thruster configurations
- Sensor integration (IMU, depth sensors)

## Network Architecture

### Local Network
- ROV components communicate over internal network
- ZMQ and UDP used for internal messaging

### ROV to Ground Communication
- Ethernet/fiber connection between ROV and surface
- Configurable IP addresses and ports in `config.py`
- Compressed video/sonar streams to manage bandwidth

## Configuration Systems

### Environment Variables
- `ROV_TYPE`: Defines the ROV configuration (affects camera setup, etc.)

### Configuration Files
- `config.py`: Central configuration parameters
- `config_pid.json` and `config_pid.py`: PID controller parameters

## Deployment Considerations

### Container Architecture
- Docker used for consistent environments
- `Dockerfile` defines build requirements
- Dev container support for development environment

### Resource Constraints
- Optimization for limited bandwidth between ROV and surface
- Consideration for processing power on embedded systems
- Real-time performance requirements (low latency) 