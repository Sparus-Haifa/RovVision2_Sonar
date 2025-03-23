# Active Context for RovVision2_Sonar

## Current Work Focus

The current development focus is on enhancing the sonar integration and display capabilities of the ROV system, as well as developing alternative camera display options that bypass the distributed ZMQ framework. Recent additions include:

1. **Sonar Data Processing**: Implementation of `sonGate.py` to handle sonar data acquisition and transmission
2. **Sonar Display**: Development of dedicated display components for sonar visualization
3. **Combined Display**: Creating a unified display that shows both camera feeds and sonar data
4. **Sonar Power Management**: Addressing issues with sonar power shutdown during system termination
5. **Direct Camera Display**: Creating a direct camera access display option that bypasses ZMQ framework

## Recent Changes

### Direct Camera Access
- Created `display_direct.py` for accessing and displaying camera feed directly without ZMQ
- Implemented direct access to IDS uEye camera with reduced resolution (1024x1024) for better performance
- Added on-screen display of camera information (FPS, exposure)
- Included interactive controls for exposure adjustment and auto-exposure toggle
- Optimized for maximum frame rate by reducing resolution and simplifying the display pipeline

### Sonar Integration
- Added `sonGate.py` for processing sonar data similar to camera data through `imGate.py`
- Implemented UDP transmission of compressed sonar images to ground control
- Added sonar display capabilities to the ground control interface
- Created specialized display components for viewing sonar data on the ROV itself
- Fixed sonar power management by modifying `sysRun.sh` to explicitly send SIGINT to enable_sonar.py before tmux kill-ser

### Interface Improvements
- Enhanced the `rovViewer.py` to support sonar image display alongside camera feeds
- Added controls for sonar-specific parameters
- Implemented image quality and compression adjustments for sonar data

### Display Systems
- Developed `display_sonar.py` for dedicated sonar visualization on the ROV
- Created `display_combined.py` for showing camera and sonar data together
- Implemented `display_feed.py` for local display of camera feeds on the ROV
- Added `display_direct.py` for direct camera access and display without ZMQ

## Active Decisions

1. **Image Compression Strategy**: Balancing image quality with bandwidth constraints for both camera and sonar data
2. **UI Layout**: Determining the optimal way to present sonar data alongside camera feeds
3. **Processing Distribution**: Deciding what processing happens onboard vs. at the ground station
4. **Synchronization**: Ensuring proper synchronization between sonar and camera data
5. **Sonar Power Management**: Modified the system shutdown process to explicitly send SIGINT to sonar processes before hard kill
6. **Camera Resolution Trade-offs**: Reducing resolution from 2048x2048 to 1024x1024 to achieve higher frame rates
7. **Display Architecture Options**: Providing both ZMQ-based distributed display and direct camera access options

## Near-Term Tasks

1. **Optimize Sonar Transmission**: Improve compression and transmission of sonar data
2. **Enhance Display Layout**: Refine the combined display of camera and sonar feeds
3. **Add Analysis Tools**: Implement tools for measuring and analyzing features in sonar data
4. **Improve UI Controls**: Add more intuitive controls for sonar parameters
5. **Test Bandwidth Usage**: Measure and optimize bandwidth consumption
6. **Optimize Camera Performance**: Further explore pixelclock and binning options to maximize frame rate
7. **Incorporate Direct Display into Main System**: Consider integrating the direct display approach into the primary system when appropriate

## Known Issues

1. **Image Quality vs. Bandwidth**: Finding the right balance for sonar image compression
2. **UI Responsiveness**: Ensuring UI remains responsive while handling multiple video streams
3. **Synchronization Delays**: Addressing potential delays between camera and sonar data
4. **Resource Usage**: Managing CPU and memory usage with additional data streams
5. **Camera Frame Rate Limitations**: Full resolution (2048x2048) camera capture limited to approximately 10 FPS

## Technical Debt

1. **Code Duplication**: Similar logic repeated in various gate modules that could be refactored
2. **Configuration Management**: Too many hardcoded values that should be moved to configuration
3. **Error Handling**: Improve robustness of network communication code
4. **Documentation**: Need better inline documentation in sonar-related components
5. **Signal Handling**: Proper handling of system signals for clean shutdown across the system - should be applied to all hardware management processes following the sonar power management pattern

## Next Major Milestones

1. Complete sonar integration and visualization components
2. Fix system shutdown issues for clean termination of all components
3. Field testing of combined camera/sonar system
4. Implement advanced sonar data analysis tools
5. Enhance autonomy features using sonar data for navigation
6. Optimize camera display and processing for maximum performance and quality 