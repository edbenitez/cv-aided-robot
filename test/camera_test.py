import numpy as np
import cv2


# create VideoCapture object and return it
def openCamera():
    return cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")


def readFromCamera(vidCapObj):
    # check if capture is initialized
    if vidCapObj.isOpened():
        windowName = "robo_eyesight" # window handle
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL) # window can be resized
        cv2.resizeWindow(windowName, 1280, 720)
        cv2.moveWindow(windowName, 0, 0)
        cv2.setWindowTitle(windowName, "Robo Eyesight")
        font = cv2.FONT_HERSHEY_PLAIN
        while cv2.getWindowProperty(windowName, 0) >= 0: # if window isn't closed by user
            ret, frame = vidCapObj.read() # returns bool and frame
            cv2.imshow(windowName, frame) # display image in specified window
            if cv2.waitKey(1) & 0xFF == ord('q'): # if user hits 'q' key
                break

        

if __name__ == "__main__":
    cap = openCamera() # get VideoCapture Object
    readFromCamera(cap) # capture and display frames
    cap.release() # close camera connection
    cv2.destroyAllWindows() # destory GUI window
