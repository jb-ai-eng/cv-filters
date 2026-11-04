import sys
import cv2
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "data" / "input" / "test.mp4"
video = cv2.VideoCapture(str(INPUT_PATH)) 
if not video.isOpened(): 
    sys.exit("Could not open the video") 
fps = video.get(cv2.CAP_PROP_FPS) 
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) 
print(f"FPS: {fps}") 
print(f"Width: {width}") 
print(f"Height: {height}") 
print(f"Frame Count: {frame_count}") 
video.release() 


