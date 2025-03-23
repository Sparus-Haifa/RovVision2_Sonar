#!/usr/bin/env python3

# switch gpio 38 (gpio 77) high to enable sonar
# when the program exits, the gpio will be set low

import RPi.GPIO as GPIO
import atexit
import time
import signal
import sys

# Define GPIO pin for sonar power
SONAR_PIN = 38

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SONAR_PIN, GPIO.OUT)
GPIO.output(SONAR_PIN, GPIO.HIGH)
print('Sonar powered ON')

# Cleanup function to ensure GPIO is properly reset
def cleanup_gpio():
    print('Cleaning up GPIO...')
    try:
        GPIO.output(SONAR_PIN, GPIO.LOW)
        GPIO.cleanup()
        print('Sonar powered OFF')
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Signal handler for various termination signals
def signal_handler(sig, frame):
    print(f'Received signal {sig}, shutting down sonar...')
    cleanup_gpio()
    sys.exit(0)

# Register signal handlers for different termination scenarios
signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
signal.signal(signal.SIGINT, signal_handler)   # Interrupt from keyboard (Ctrl+C)
signal.signal(signal.SIGHUP, signal_handler)   # Hangup signal (sent by tmux kill-session)

# Register atexit handler as a backup cleanup method
atexit.register(cleanup_gpio)

# Keep the program running and poll for interrupts
try:
    while True:
        time.sleep(5)
        print('Sonar is ON')
except Exception as e:
    print(f"Error in main loop: {e}")
finally:
    # This ensures cleanup happens even if an exception occurs
    cleanup_gpio()
