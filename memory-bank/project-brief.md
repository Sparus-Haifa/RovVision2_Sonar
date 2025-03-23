# RovVision2_Sonar Project Structure
# This file documents the key directories and their purposes

# Core Directories
/onboard/        # Code that runs on the ROV itself
/ground_control/ # Code for the ground control station
/hw/             # Hardware-specific code and drivers
/utils/          # Shared utility functions
/plugins/        # Plugin modules for additional functionality
/scripts/        # Utility scripts
/web/            # Web interface components
/sim/            # Simulation-related code

# Key Files
/config.py       # Main configuration file
/zmq_topics.py   # ZMQ messaging topics definitions

# Camera-Related Components
/onboard/imGate.py      # Image processing and distribution
/onboard/sonGate.py     # Sonar image processing
/ground_control/rovViewer.py  # Ground control viewer

# New Components
/onboard/display_feed.py  # Local ROV display of camera feed 