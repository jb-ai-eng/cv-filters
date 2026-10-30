"""
Level 1: Real-time webcam filters.

Usage:
    python filters.py              -> uses the webcam
    python filters.py photo.jpg    -> applies the filters to an image

Keys:
    0 normal | 1 gray | 2 blur | 3 edges | 4 sepia | 5 cartoon | 6 negative
    s save screenshot | q quit
"""
import sys
import cv2
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "face_detection_yunet.onnx"
FACE_DETECTOR = cv2.FaceDetectorYN.create(
    str(MODEL_PATH), "", (320, 240)
) 
FACE_DETECTOR.setScoreThreshold(0.6) 


# ---------- FILTERS ----------
# Each filter takes a BGR image (OpenCV stores colors as Blue, Green, Red)
# and returns another BGR image of the same size.

def normal(img):
    return img


def gray(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Back to 3 channels so every filter returns the same format
    return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)


def blur(img):
    k = cv2.getTrackbarPos("Blur","CV Filters") 
    if k % 2 == 0:
        k = k+ 1
    # Blur size comes from the slider; it must be odd, so we fix even values
    return cv2.GaussianBlur(img, (k, k), 0)


def edges(img):
    
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h = cv2.getTrackbarPos("Edges","CV Filters")
    e = cv2.Canny(g, h, 200)  # thresholds: lower them to see more edges
    return cv2.cvtColor(e, cv2.COLOR_GRAY2BGR)


def sepia(img):
    # An image is just a matrix of numbers: here we mix the channels
    # with a 3x3 matrix (each row = new B, G, R).
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    return cv2.transform(img, kernel).clip(0, 255).astype(np.uint8)


def negative(img):
    return 255 - img


def cartoon(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.medianBlur(g, 7)
    lines = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)
    colors = cv2.bilateralFilter(img, 9, 250, 250)
    return cv2.bitwise_and(colors, colors, mask=lines)


def face_box(img):
    h, w = img.shape[:2]
    FACE_DETECTOR.setInputSize((w, h))
    _, faces = FACE_DETECTOR.detect(img)
    out = img.copy()
    if faces is not None:
        for face in faces:
            x, y, fw, fh = face[:4].astype(int)
            cv2.rectangle(out, (x, y), (x + fw, y + fh), (0, 255, 0), 2)
            points = face[4:14].reshape(5, 2).astype(int)
            cv2.circle(out, tuple(points[0]), 4, (255, 0, 0), -1)    # right eye
            cv2.circle(out, tuple(points[1]), 4, (255, 0, 0), -1)    # left eye
            cv2.circle(out, tuple(points[2]), 4, (0, 255, 255), -1)  # nose
            cv2.circle(out, tuple(points[3]), 4, (0, 0, 255), -1)    # mouth right
            cv2.circle(out, tuple(points[4]), 4, (0, 0, 255), -1)    # mouth left
    return out


def anonymize(img):
    h, w = img.shape[:2]
    FACE_DETECTOR.setInputSize((w, h))
    _, faces = FACE_DETECTOR.detect(img)
    out = img.copy()
    if faces is not None:
        for face in faces:
            x, y, fw, fh = face[:4].astype(int)
            x, y = max(x, 0), max(y, 0)
            roi = out[y:y + fh, x:x + fw]
            b = cv2.GaussianBlur(roi, (51, 51 ), 0) 
            out [y:y + fh, x:x + fw]= b
    return out


FILTERS = {
    ord("0"): ("Normal", normal),
    ord("1"): ("Gray", gray),
    ord("2"): ("Blur", blur),
    ord("3"): ("Edges", edges),
    ord("4"): ("Sepia", sepia),
    ord("5"): ("Cartoon", cartoon),
    ord("6"): ("Negative", negative),
    ord("7"): ("Face", face_box),
    ord("8"): ("Anonymize", anonymize),
}


# ---------- PROGRAM ----------

def draw_label(img, text):
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


def main():
    name, apply_filter = FILTERS[ord("0")]
    still_image = None

    if len(sys.argv) > 1:
        still_image = cv2.imread(sys.argv[1])
        if still_image is None:
            sys.exit(f"Could not open {sys.argv[1]}")
    else:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            sys.exit("Could not open the webcam (check Terminal's camera permission)")

    cv2.namedWindow("CV Filters")
    cv2.createTrackbar("Blur","CV Filters", 21, 99, lambda v: None) 
    cv2.createTrackbar("Edges","CV Filters", 100, 255, lambda v: None) 

    shots = 0
    while True:
        if still_image is not None:
            frame = still_image.copy()
        else:
            ok, frame = cam.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)  # mirror effect

        output = apply_filter(frame)
        draw_label(output, name)
        cv2.imshow("CV Filters", output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            filename = f"capture_{shots}.png"
            cv2.imwrite(filename, output)
            print("Saved:", filename)
            shots += 1
        elif key in FILTERS:
            name, apply_filter = FILTERS[key]

    if still_image is None:
        cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
