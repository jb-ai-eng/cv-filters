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
    # (21, 21) is the "brush" size; it must be odd. Try changing it.
    return cv2.GaussianBlur(img, (21, 21), 0)


def edges(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    e = cv2.Canny(g, 100, 200)  # thresholds: lower them to see more edges
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
    # TODO (your exercise): combine what already exists.
    #   1. Get the edges with cv2.adaptiveThreshold on the gray image
    #      smoothed with cv2.medianBlur(gray, 7)
    #   2. Smooth the colors with cv2.bilateralFilter(img, 9, 250, 250)
    #   3. Combine both with cv2.bitwise_and(colors, colors, mask=edges)
    # Until you do it, return the image unchanged.
    return img


FILTERS = {
    ord("0"): ("Normal", normal),
    ord("1"): ("Gray", gray),
    ord("2"): ("Blur", blur),
    ord("3"): ("Edges", edges),
    ord("4"): ("Sepia", sepia),
    ord("5"): ("Cartoon", cartoon),
    ord("6"): ("Negative", negative),
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
