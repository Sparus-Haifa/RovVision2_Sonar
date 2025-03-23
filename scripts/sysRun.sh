#!/bin/bash

if [ "$1" = "kill" ]; then
    echo "Gracefully stopping system..."
    
    # First attempt to gracefully stop processes with SIGINT
    # Find and send SIGINT to enable_sonar.py
    echo "Sending SIGINT to sonar process..."
    SONAR_PID=$(pgrep -f "enable_sonar.py")
    if [ ! -z "$SONAR_PID" ]; then
        echo "Sending SIGINT to sonar process $SONAR_PID"
        kill -INT $SONAR_PID
        sleep 2  # Give it time to clean up
    else
        echo "No sonar process found"
    fi
    
    # Also send SIGINT to remote sonar process
    echo "Sending SIGINT to remote sonar process..."
    ssh $REMOTE_SUB "SONAR_PID=\$(pgrep -f \"enable_sonar.py\"); if [ ! -z \"\$SONAR_PID\" ]; then echo \"Sending SIGINT to remote sonar process \$SONAR_PID\"; kill -INT \$SONAR_PID; sleep 2; else echo \"No remote sonar process found\"; fi"
    
    # Then use tmux kill-ser for the remaining processes
    echo "Now stopping remaining processes..."
    tmux kill-ser
    sleep 1
    ssh $REMOTE_SUB "tmux kill-ser"
    exit 1
fi

# Existing code for startup
tmux kill-ser
sleep 1

# run remote code only if tmux is not running
if ssh $REMOTE_SUB "tmux info &> /dev/null"; then 
    echo remote tmux is running
    # exit 0
else
    echo remote tmux is not running
    # exit 1
    ./run_remote.sh
    sleep 10
fi

./run_ground_control.sh
