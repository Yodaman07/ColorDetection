import cv2 as cv
import numpy as np

# basic camera code is copied from one of my previous projects https://github.com/Yodaman07/HandWrittenNumbers/blob/main/main.py
# massive help from https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html and https://www.youtube.com/watch?v=ddSo8Nb0mTw

color = np.uint8([[[255, 0, 0]]])


def ColorPicker(event, x: int, y: int, flags, img: np.ndarray):  # Callback
    global color
    if event == cv.EVENT_LBUTTONDOWN:
        pixel_color = img[y][x]  # BGR Color
        # As x increases, the pixel moves to the right
        # As y increases, the pixel moves down
        # img[0][0] is the pixel in the top left most corner
        color = np.uint8([[pixel_color]])
        print(f"Updating color mask to match at ({x},{y})")


cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Unable to access camera")  # kill the program if the camera is not accessed
    cam.release()
    exit()

while True:
    # a = Adjuster()
    retrieved, frame = cam.read()
    if not retrieved:
        print("Stream has likely ended")
        break

    # a single pixel in a BGR format
    hsvColor = cv.cvtColor(color, cv.COLOR_BGR2HSV)
    hue = hsvColor[0][0][0]

    lower_bound = np.uint8([hue - 25, 50, 50])
    upper_bound = np.uint8([hue + 25, 255, 255])

    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsvFrame, lower_bound, upper_bound)

    cv.setMouseCallback("stream", ColorPicker, param=frame)
    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow("mask", res)
    cv.imshow("stream", frame)

    # https://stackoverflow.com/questions/5217519/what-does-opencvs-cvwaitkey-function-do <-- how waitKey works
    if cv.waitKey(1) == ord("q"):  # gets the unicode value for q
        break

cam.release()
cv.destroyAllWindows()
