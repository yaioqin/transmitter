import pyrealsense2 as rs
import numpy as np
import cv2
import os

def capture_and_save_realsense_frames():
    """
    Capture one frame of RGB and Depth images from Intel RealSense camera and save as PNG files.

    Args:
        output_folder (str): Directory to save the captured images. Defaults to "realsense_capture".

    Returns:
        tuple: (success, message) where success is boolean indicating if capture was successful
    """
    # Create output directory if it doesn't exist

    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    try:
        # Start streaming
        pipeline.start(config)
        
        for _ in range(2):
            pipeline.wait_for_frames()
            
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return (False, "Failed to get depth or color frame")

        # Convert images to numpy arrays
        """
        Depth frame dimensions: (480, 640)
        Depth frame width: 640
        Depth frame height: 480
        """
        depth_image = np.asanyarray(depth_frame.get_data()) 
        
        """
        Color frame dimensions: (480, 640, 3)
        Color frame width: 640
        Color frame height: 480
        """
        color_image = np.asanyarray(color_frame.get_data())

        return color_image,depth_image

    except Exception as e:
        return (False, f"Error: {str(e)}")
    finally:
        # Stop streaming
        pipeline.stop()

# Example usage:
# if __name__ == "__main__":
#     success, message = capture_and_save_realsense_frames()
#     print(message)