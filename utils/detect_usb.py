import os
import pickle
import subprocess
import glob
import re

if __name__=='__main__':
    dmap = {}
    rov_type = int(os.environ.get('ROV_TYPE','1'))
    
    # First, check which ttyUSB devices actually exist
    available_devices = glob.glob('/dev/ttyUSB*')
    print(f"Available devices: {available_devices}")
    
    if not available_devices:
        print("No USB devices found!")
    
    for dev in available_devices:
        try:
            print(f"\nProcessing device: {dev}")
            
            # Get device information using more direct commands
            # Use lsusb to get vendor and product IDs
            cmd1 = f"udevadm info -a -n {dev} | grep -i 'ATTRS{{manufacturer}}' | head -n 1"
            cmd2 = f"udevadm info -a -n {dev} | grep -i 'ATTRS{{product}}' | head -n 1"
            cmd3 = f"udevadm info -a -n {dev} | grep -i 'KERNELS'"
            
            # Run commands and get output
            mfr = os.popen(cmd1).read().strip()
            prod = os.popen(cmd2).read().strip()
            kernels = os.popen(cmd3).read().strip()
            
            print("Manufacturer info:", mfr)
            print("Product info:", prod)
            print("Kernel path info:", kernels)
            
            # Extract product name if available
            product = None
            if prod:
                match = re.search(r'ATTRS{product}=="([^"]+)"', prod)
                if match:
                    product = match.group(1)
            
            # Extract USB path from kernels info
            usb_path = None
            for line in kernels.split('\n'):
                if 'usb' in line and 'KERNELS' in line:
                    match = re.search(r'KERNELS=="([^"]+)"', line)
                    if match:
                        usb_path = match.group(1)
                        if match.group(1).startswith('1-'):
                            break
            
            print(f"Extracted information:")
            print(f"  USB Path: {usb_path}")
            print(f"  Product: {product}")
            
            # Map devices based on USB path or product name
            if rov_type == 4:
                # Primary method: Identify by product name
                if product:
                    if "USB-RS232 Cable" in product or "RS232" in product:
                        dmap['VNAV_USB'] = dev
                        print(f"  Mapped as VNAV_USB (Vectornav) by product name")
                    elif "TTL232R" in product or "TTL232" in product:
                        dmap['ESC_USB'] = dev
                        print(f"  Mapped as ESC_USB (ESP32) by product name")
                
                # Fallback method: if we have path information
                elif usb_path:
                    parts = usb_path.split(':')
                    for part in parts:
                        if '1-2.2' in part:
                            dmap['VNAV_USB'] = dev
                            print(f"  Mapped as VNAV_USB (Vectornav) by path")
                        elif '1-2.4' in part:
                            dmap['ESC_USB'] = dev
                            print(f"  Mapped as ESC_USB (ESP32) by path")
                
                # Last resort: Use a heuristic based on device node
                # Assuming ttyUSB0 is typically Vectornav and ttyUSB1 is ESP32
                if 'VNAV_USB' not in dmap and 'ESC_USB' not in dmap:
                    if dev.endswith('0'):
                        dmap['VNAV_USB'] = dev
                        print(f"  Mapped as VNAV_USB (Vectornav) by device number")
                    elif dev.endswith('1'):
                        dmap['ESC_USB'] = dev
                        print(f"  Mapped as ESC_USB (ESP32) by device number")
            
            # Keep the other ROV type mappings
            elif rov_type == 1:
                # ROV type 1 mappings
                if usb_path and '1-7' in usb_path:
                    dmap['SONAR_USB'] = dev
                elif usb_path and '1-5' in usb_path:
                    dmap['ESC_USB'] = dev
                elif usb_path and '1-3' in usb_path:
                    dmap['VNAV_USB'] = dev
                elif usb_path and '1-1' in usb_path:
                    dmap['PERI_USB'] = dev
            
            elif rov_type == 2:
                # ROV type 2 mappings
                if usb_path and '1-5.4' in usb_path:
                    dmap['SONAR_USB'] = dev
                elif usb_path and '1-5.1' in usb_path:
                    dmap['PERI_USB'] = dev
                elif usb_path and '1-5.2' in usb_path:
                    dmap['VNAV_USB'] = dev
                elif usb_path and '1-5.3' in usb_path:
                    dmap['ESC_USB'] = dev
            
            elif rov_type == 3:
                # ROV type 3 mappings
                if usb_path and '1-5.4' in usb_path:
                    dmap['SONAR_USB'] = dev
                elif usb_path and '1-5.1' in usb_path:
                    dmap['PERI_USB'] = dev
                elif usb_path and '1-5.2' in usb_path:
                    dmap['VNAV_USB'] = dev
                elif usb_path and '1-5.3' in usb_path:
                    dmap['ESC_USB'] = dev
        
        except Exception as e:
            print(f"Error processing device {dev}: {e}")
    
    # Save the device map
    with open('/tmp/devusbmap.pkl', 'wb') as fp:
        pickle.dump(dmap, fp)
        print('\nFinal device map = ', dmap)

else:
    if not os.path.isfile('/tmp/devusbmap.pkl'):
        print('Error cannot find /tmp/devusbmap.pkl please run detect_usb.py')
    devmap = pickle.load(open('/tmp/devusbmap.pkl', 'rb'))

