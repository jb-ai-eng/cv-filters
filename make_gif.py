import argparse
import sys
import cv2
from pathlib import Path
from PIL import Image
INPUT_PATH = Path(__file__).parent / "data" / "output" / "demo_box.mp4"
OUTPUT_PATH = Path(__file__).parent / "assets" / "demo.gif"
parser = argparse.ArgumentParser()
parser.add_argument("--input", type=Path, default=INPUT_PATH)
parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
parser.add_argument("--top", type=float, default=0.35)
parser.add_argument("--bottom", type=float, default=1.0)
parser.add_argument("--every", type=int, default=2)
parser.add_argument("--seconds", type=float, default=6.0)
args = parser.parse_args()
video = cv2.VideoCapture(str(args.input)) 
if not video.isOpened(): 
    sys.exit("Could not open the video") 
fps = video.get(cv2.CAP_PROP_FPS)
frames_read = 0
frames = []
while True:
    ok, frame = video.read()
    if not ok:
        break
    frames_read += 1
    if frames_read > args.seconds * fps:
        break
    if frames_read % args.every != 0:
        continue
    h, w = frame.shape[:2]
    frame = frame[int(h * args.top):int(h * args.bottom), :]
    new_h = int(frame.shape[0] * 480 / w)
    small = cv2.resize(frame, (480, new_h))
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    frames.append(Image.fromarray(rgb))
print(f"Frames read: {frames_read}, FPS: {fps}, frames in list: {len(frames)}")
video.release()
args.output.parent.mkdir(exist_ok=True)
duration = int(1000 * args.every / fps)
frames[0].save(args.output, save_all=True, append_images=frames[1:], duration=duration, loop=0)
print(f"Saved: {args.output}")
