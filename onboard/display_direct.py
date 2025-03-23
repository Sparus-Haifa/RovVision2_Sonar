#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os
os.environ['DISPLAY'] = ':0'

import numpy as np
import sys
import time
import cv2
import argparse

# Add paths for camera and utilities
sys.path.append('..')
sys.path.append('../utils')
sys.path.append('../hw/idsCam/')

# Import camera module for direct access
from camera import Camera
from pyueye import ueye
import config

# Parse command line arguments
parser = argparse.ArgumentParser(description='ROV Direct Camera Display')
parser.add_argument('--windowed', action='store_true', help='Run in windowed mode (with window decorations)')
parser.add_argument('--width', type=int, default=1080, help='Display width (default: 1080 - portrait mode)')
parser.add_argument('--height', type=int, default=1920, help='Display height (default: 1920 - portrait mode)')
parser.add_argument('--cam-ratio', type=float, default=1.0, help='Ratio of screen height for camera (0.0-1.0, default: 1.0)')
parser.add_argument('--margin', type=int, default=10, help='Margin in pixels (default: 10)')
parser.add_argument('--fps', type=float, default=30.0, help='Camera FPS (default: 30.0)')
args = parser.parse_args()

# Keep track of program state
keep_running = True
fps_counter = 0
fps_timer = time.time()
current_fps = 0

def resize_to_width(img, target_width):
    """Resize image to target width maintaining aspect ratio"""
    h, w = img.shape[:2]
    ratio = target_width / w
    target_height = int(h * ratio)
    return cv2.resize(img, (target_width, target_height))

def draw_glowing_text(img, text, pos, color, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1.0, thickness=2):
    """Draw text with a glowing effect"""
    # Draw glow (larger black outline)
    for offset in [(2,2), (-2,2), (2,-2), (-2,-2)]:
        x = pos[0] + offset[0]
        y = pos[1] + offset[1]
        cv2.putText(img, text, (x, y), font, font_scale, (0,0,0), thickness+2)
    
    # Draw white outline for better contrast
    cv2.putText(img, text, pos, font, font_scale, (255,255,255), thickness+1)
    # Draw main text
    cv2.putText(img, text, pos, font, font_scale, color, thickness)

def init_camera():
    """Initialize the camera with appropriate settings"""
    print("Initializing camera...")
    cam = Camera(device_id=0, buffer_count=3)
    cam.init()
    
    # Set camera mode to RAW8 (same as in camIds.py)
    cam.set_colormode(ueye.IS_CM_SENSOR_RAW8)
    
    # Set camera resolution to 1024x1024 (reduced from 2048x2048)
    ret = cam.set_aoi(0, 0, 1024, 1024)
    cam.alloc()
    
    # Set frame rate
    cam.set_fps(args.fps)
    
    # Print camera info
    print(f"Camera initialized:")
    print(f'FPS: {cam.get_fps()}')
    print(f'Available FPS range: {cam.get_fps_range()}')
    print(f'Pixelclock: {cam.get_pixelclock()}')
    
    # Set initial exposure
    cam.set_exposure_auto(1)  # Auto exposure on
    
    return cam

def display_camera():
    """Main function to capture and display camera feed"""
    global keep_running, fps_counter, fps_timer, current_fps
    
    # Initialize camera
    try:
        cam = init_camera()
    except Exception as e:
        print(f"Error initializing camera: {e}")
        return
    
    # Create window
    window_name = 'Direct Camera Feed'
    if not args.windowed:  # Windowless is the default
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, args.width, args.height)
    
    # Display area calculations
    cam_height = int(args.height * args.cam_ratio)
    
    # Exposure controls
    exposure = float(cam.get_exposure())  # Convert to Python float
    exposure_step = 0.3
    auto_exposure = 1  # Start with auto exposure on
    
    print("Starting capture loop...")
    print("Press 'q' to quit, '+'/'-' to adjust exposure, 'a' to toggle auto exposure")
    
    frame_count = 0
    
    while keep_running:
        try:
            # Capture image directly from camera
            image, timestamp = cam.capture_image()
            
            if image is not None:
                # Convert Bayer pattern to BGR (for OpenCV display)
                img_bgr = cv2.cvtColor(image.astype('uint8'), cv2.COLOR_BAYER_BG2BGR)
                
                # Create display image
                display_img = np.zeros((args.height, args.width, 3), dtype=np.uint8)
                
                # Resize camera image maintaining aspect ratio
                camera_resized = resize_to_width(img_bgr, args.width)
                if camera_resized.shape[0] > cam_height:
                    # If too tall, crop from center
                    start = (camera_resized.shape[0] - cam_height) // 2
                    camera_resized = camera_resized[start:start + cam_height]
                else:
                    # If too short, center vertically
                    start = (cam_height - camera_resized.shape[0]) // 2
                    display_img[start:start + camera_resized.shape[0], :] = camera_resized
                    camera_resized = None  # Mark as handled
                
                if camera_resized is not None:
                    display_img[0:cam_height, :] = camera_resized
                
                # Update FPS counter
                fps_counter += 1
                if time.time() - fps_timer > 3:
                    current_fps = fps_counter / (time.time() - fps_timer)
                    fps_counter = 0
                    fps_timer = time.time()
                    # Update current exposure value and convert to Python float
                    exposure = float(cam.get_exposure())
                    print(f"FPS: {current_fps:.2f}, Exposure: {exposure:.2f}")
                
                # Add status indicators
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8
                thickness = 2
                line_height = 35
                
                # Display FPS
                draw_glowing_text(display_img, f'FPS: {current_fps:.1f}', 
                                 (10, line_height), 
                                 (0, 255, 0), font, font_scale, thickness)
                
                # Display exposure status - ensure exposure is a Python float for formatting
                exp_text = f"Exposure: {float(exposure):.1f} (AUTO)" if auto_exposure else f"Exposure: {float(exposure):.1f}"
                draw_glowing_text(display_img, exp_text, 
                                 (250, line_height), 
                                 (0, 255, 0), font, font_scale, thickness)
                
                # Display frame
                cv2.imshow(window_name, display_img)
                frame_count += 1
            
            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                keep_running = False
            elif key == ord('+'):
                if not auto_exposure:
                    exposure = float(exposure) + exposure_step
                    print(f"Setting exposure to: {float(exposure):.2f}")
                    exposure = cam.set_exposure(exposure)
                    exposure = float(exposure)  # Convert result back to Python float
            elif key == ord('-'):
                if not auto_exposure:
                    exposure = max(1, float(exposure) - exposure_step)
                    print(f"Setting exposure to: {float(exposure):.2f}")
                    exposure = cam.set_exposure(exposure)
                    exposure = float(exposure)  # Convert result back to Python float
            elif key == ord('a'):
                auto_exposure = 1 - auto_exposure  # Toggle between 0 and 1
                cam.set_exposure_auto(auto_exposure)
                print(f"Auto exposure {'enabled' if auto_exposure else 'disabled'}")
            
        except KeyboardInterrupt:
            keep_running = False
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Wait a bit before retrying

    # Clean up
    cv2.destroyAllWindows()
    cam.exit()
    print("Camera display stopped.")

if __name__ == '__main__':
    try:
        display_camera()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}") 