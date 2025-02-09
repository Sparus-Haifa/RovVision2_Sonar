#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
import zmq
import sys
import asyncio
import time
import pickle
import cv2
import argparse

sys.path.append('..')
sys.path.append('../utils')
import zmq_wrapper
import zmq_topics
import config

# Parse command line arguments
parser = argparse.ArgumentParser(description='ROV Combined Camera and Sonar Display')
parser.add_argument('--windowless', action='store_true', help='Run in windowless mode (no window decorations)')
parser.add_argument('--width', type=int, default=1080, help='Display width (default: 1080 - portrait mode)')
parser.add_argument('--height', type=int, default=1920, help='Display height (default: 1920 - portrait mode)')
parser.add_argument('--cam-ratio', type=float, default=0.6, help='Ratio of screen height for camera (0.0-1.0, default: 0.6)')
parser.add_argument('--margin', type=int, default=10, help='Margin between images in pixels (default: 10)')
args = parser.parse_args()

# Subscribe to both camera and sonar feeds
subs_socks = []
subs_socks.append(zmq_wrapper.subscribe([zmq_topics.topic_stereo_camera], zmq_topics.topic_camera_port))
subs_socks.append(zmq_wrapper.subscribe([zmq_topics.topic_sonar], zmq_topics.topic_sonar_port))
keep_running = True

# Initialize image placeholders
camera_img = None
sonar_img = None

def resize_to_width(img, target_width):
    """Resize image to target width maintaining aspect ratio"""
    h, w = img.shape[:2]
    ratio = target_width / w
    target_height = int(h * ratio)
    return cv2.resize(img, (target_width, target_height))

async def display_feeds():
    global keep_running, camera_img, sonar_img
    
    # Create window
    window_name = 'Combined Feed'
    if args.windowless:
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, args.width, args.height)
    
    # Calculate fixed heights for camera and sonar
    cam_height = int(args.height * args.cam_ratio)
    sonar_height = args.height - cam_height - args.margin
    
    while keep_running:
        try:
            socks = zmq.select(subs_socks, [], [], 0.005)[0]
            for sock in socks:
                ret = sock.recv_multipart()
                
                # Process camera feed
                if ret[0] == zmq_topics.topic_stereo_camera:
                    frame_cnt, shape, ts, camState, hasHighRes = pickle.loads(ret[1])
                    camera_img = np.frombuffer(ret[-2], 'uint8').reshape((shape[0]//2, shape[1]//2, 3)).copy()
                
                # Process sonar feed
                elif ret[0] == zmq_topics.topic_sonar:
                    frame_cnt, shape, ts, camState, hasHighRes = pickle.loads(ret[1])
                    sonar_img = np.frombuffer(ret[-2], 'uint8').reshape((shape[0]//2, shape[1]//2, 3)).copy()
            
            # Combine and display images if both are available
            if camera_img is not None and sonar_img is not None:
                # Create black background
                combined = np.zeros((args.height, args.width, 3), dtype=np.uint8)
                
                # Resize camera image maintaining aspect ratio
                cam_resized = resize_to_width(camera_img, args.width)
                if cam_resized.shape[0] > cam_height:
                    # If too tall, crop from center
                    start = (cam_resized.shape[0] - cam_height) // 2
                    cam_resized = cam_resized[start:start + cam_height]
                else:
                    # If too short, center vertically
                    start = (cam_height - cam_resized.shape[0]) // 2
                    combined[start:start + cam_resized.shape[0], :] = cam_resized
                    cam_resized = None  # Mark as handled
                
                if cam_resized is not None:
                    combined[0:cam_height, :] = cam_resized
                
                # Resize sonar image maintaining aspect ratio
                sonar_resized = resize_to_width(sonar_img, args.width)
                if sonar_resized.shape[0] > sonar_height:
                    # If too tall, crop from center
                    start = (sonar_resized.shape[0] - sonar_height) // 2
                    sonar_resized = sonar_resized[start:start + sonar_height]
                else:
                    # If too short, center vertically
                    start = cam_height + args.margin + (sonar_height - sonar_resized.shape[0]) // 2
                    combined[start:start + sonar_resized.shape[0], :] = sonar_resized
                    sonar_resized = None  # Mark as handled
                
                if sonar_resized is not None:
                    combined[cam_height + args.margin:, :] = sonar_resized
                
                # Display combined image
                cv2.imshow(window_name, combined)
                cv2.waitKey(1)
            
            await asyncio.sleep(0.001)
            
        except KeyboardInterrupt:
            keep_running = False
            break
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1)  # Wait a bit before retrying

async def main():
    try:
        await display_feeds()
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # Use older asyncio pattern for compatibility
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close() 