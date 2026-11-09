import argparse
import sys
import cv2
from pathlib import Path
from filters import detect_faces, cover_faces
INPUT_PATH = Path(__file__).parent / "data" / "input" / "test.mp4"
OUTPUT_PATH = Path(__file__).parent / "data" / "output" / "test_anonymize.mp4"
parser = argparse.ArgumentParser()
parser.add_argument("--method", choices=["blur", "pixelate", "box"], default="blur")
parser.add_argument("--input", type=Path, default=INPUT_PATH)
parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
parser.add_argument("--hold", type=int, default=5)
args = parser.parse_args()
if args.hold < 1:
    sys.exit("--hold must be 1 or more")
video = cv2.VideoCapture(str(args.input)) 
if not video.isOpened(): 
    sys.exit("Could not open the video") 
fps = video.get(cv2.CAP_PROP_FPS) 
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
writer = cv2.VideoWriter(str(args.output), fourcc, fps, (width, height))
if not writer.isOpened(): 
    sys.exit("Could not create the output video")
print(f"FPS: {fps}") 
print(f"Width: {width}") 
print(f"Height: {height}") 
print(f"Frame Count: {frame_count}") 
frames_read = 0
recent = []
while True: 
    ok, frame = video.read() 
    if not ok: 
        break                               
    frames_read += 1 
    boxes = detect_faces(frame)
    recent.append(boxes)
    if len(recent) > args.hold:
        recent.pop(0)
    all_boxes = []
    for frame_boxes in recent:
        all_boxes.extend(frame_boxes)
    frame = cover_faces(frame, all_boxes, args.method)

    writer.write(frame)
print(f"Frames read: {frames_read}")
video.release() 
writer.release()

