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
parser = argparse.ArgumentParser(description='ROV Camera Display')
parser.add_argument('--window-name', default='ROV Camera Feed', help='Name of the display window')
parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
args = parser.parse_args()

# Subscribe to camera feed
subs_socks = []
subs_socks.append(zmq_wrapper.subscribe([zmq_topics.topic_stereo_camera], zmq_topics.topic_camera_port))
keep_running = True

async def display_feed():
    global keep_running
    
    # Create display window
    if args.fullscreen:
        cv2.namedWindow(args.window_name, cv2.WINDOW_FULLSCREEN)
    else:
        cv2.namedWindow(args.window_name, cv2.WINDOW_NORMAL)
    
    while keep_running:
        socks = zmq.select(subs_socks, [], [], 0.005)[0]
        for sock in socks:
            ret = sock.recv_multipart()
            if ret[0] == zmq_topics.topic_stereo_camera:
                print("Received stereo camera message")
                frame_cnt, shape, ts, camState, hasHighRes = pickle.loads(ret[1])
                # Get the left camera image (using half resolution for display)
                imgl = np.frombuffer(ret[-2], 'uint8').reshape((shape[0]//2, shape[1]//2, 3)).copy()
                
                # Display the image
                cv2.imshow(args.window_name, imgl)
                key = cv2.waitKey(1) & 0xFF
                
                # Handle key presses
                if key == ord('q') or key == 27:  # 'q' or ESC to quit
                    keep_running = False
                    break
                elif key == ord('f'):  # 'f' to toggle fullscreen
                    if args.fullscreen:
                        cv2.setWindowProperty(args.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                        args.fullscreen = False
                    else:
                        cv2.setWindowProperty(args.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        args.fullscreen = True
        
        await asyncio.sleep(0.001)

async def main():
    try:
        await display_feed()
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