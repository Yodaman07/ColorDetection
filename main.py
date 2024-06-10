import cv2 as cv
import numpy
import numpy as np

# basic camera code is copied from one of my previous projects https://github.com/Yodaman07/HandWrittenNumbers/blob/main/main.py
# massive help from https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html and https://www.youtube.com/watch?v=ddSo8Nb0mTw

color = np.uint8([[[255, 0, 0]]])


def ColorPicker(event, x: int, y: int, flags, img: numpy.ndarray):  # Callback
    global color
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_color = img[y][x]  # BGR Color
        color = np.uint8([[pixel_color]])
        print(f"Updating color mask to match at ({x},{y})")


cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Unable to access camera")  # kill the program if the camera is not accessed
    cam.release()
    exit()

while True:
    retrieved, frame = cam.read()
    if not retrieved:
        print("Stream has likely ended")
        break

    # a single pixel in a BGR format
    hsvColor = cv.cvtColor(color, cv.COLOR_BGR2HSV)
    hue = hsvColor[0][0][0]

    lower_bound = np.uint8([[[hue - 10, 50, 50]]])
    upper_bound = np.uint8([[[hue + 10, 255, 255]]])

    mask = cv.inRange(frame, lower_bound, upper_bound)

    cv.setMouseCallback("stream", ColorPicker, param=frame)

    cv.imshow("stream", frame)
    cv.imshow("mask", mask)
    # https://stackoverflow.com/questions/5217519/what-does-opencvs-cvwaitkey-function-do <-- how waitKey works
    if cv.waitKey(1) == ord("q"):  # gets the unicode value for q
        break

cam.release()
cv.destroyAllWindows()
