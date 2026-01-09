import bosdyn.client
import bosdyn.client.util
from bosdyn.client.image import ImageClient
import cv2
import numpy as np
import os
from datetime import datetime

def capture_all_sensors(robot, base_path):
    # 1. Ensure the directory exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Created directory: {base_path}")

    # 2. Create a sub-folder for this specific snapshot session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = os.path.join(base_path, f"snapshot_{timestamp}")
    os.makedirs(session_dir)

    # 3. Initialize the Image Client
    image_client = robot.ensure_client(ImageClient.default_service_name)

    # List of all sensors you requested
    sources = [
        'frontleft_fisheye_image', 'frontright_fisheye_image', 
        'left_fisheye_image', 'right_fisheye_image', 'back_fisheye_image',
        'pano', 'ptz', 'ir', 'thermal'
    ]

    print(f"Capturing all sensors to: {session_dir}")
    
    # Request images from the robot
    image_responses = image_client.get_image_from_sources(sources)

    for response in image_responses:
        source_name = response.source.name
        
        if not response.shot.image.data:
            print(f"Skipping {source_name}: No data.")
            continue

        try:
            # Decode JPEG data
            img = cv2.imdecode(np.frombuffer(response.shot.image.data, dtype=np.uint8), -1)
            
            if img is None:
                print(f"Failed to decode {source_name}")
                continue

            # 4. Save to the specific folder
            file_path = os.path.join(session_dir, f"{source_name}.jpg")
            cv2.imwrite(file_path, img)
            print(f"Saved: {file_path}")
            
        except Exception as e:
            print(f"Error processing {source_name}: {e}")

def main():
    sdk = bosdyn.client.create_standard_sdk("AllSensorCapture")
    
    # Your Robot Config
    robot_ip = '10.55.203.25' 
    save_location = '/home/jawblade/Follow-Images'
    
    robot = sdk.create_robot(robot_ip)
    robot.authenticate('Bumble-Bee', 'Bumble-Bee1!')

    capture_all_sensors(robot, save_location)

if __name__ == "__main__":
    main()