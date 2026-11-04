import sys
import cv2
from pathlib import Path

INPUT_PATH = Path(__file__).parent / "data" / "input" / "test.mp4"
OUTPUT_PATH = Path(__file__).parent / "data" / "output" / "test_anonymize.mp4"
video = cv2.VideoCapture(str(INPUT_PATH)) 
if not video.isOpened(): 
    sys.exit("Could not open the video") 
fps = video.get(cv2.CAP_PROP_FPS) 
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
writer = cv2.VideoWriter(str(OUTPUT_PATH), fourcc, fps, (width, height))
if not writer.isOpened(): 
    sys.exit("Could not create the output video")
print(f"FPS: {fps}") 
print(f"Width: {width}") 
print(f"Height: {height}") 
print(f"Frame Count: {frame_count}") 
frames_read = 0 
while True: 
    ok, frame = video.read() 
    if not ok: 
        break                               
    frames_read += 1 
    writer.write(frame)
print(f"Frames read: {frames_read}")
video.release() 
writer.release()

