import numpy as np
import cv2
import sys

# create VideoCapture object and return it
def openCamera():
    return cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")


def readFromCamera(vidCapObj):
    from object_detect import ObjectDetector
    from utils import vis
    # check if capture is initialized
    if vidCapObj.isOpened():
        windowName = "robo_eyesight" # window handle
        cv2.namedWindow(windowName, cv2.WINDOW_NORMAL) # window can be resized
        cv2.resizeWindow(windowName, 500, 400)
        cv2.moveWindow(windowName, 0, 0)
        cv2.setWindowTitle(windowName, "Robo Eyesight")
        font = cv2.FONT_HERSHEY_PLAIN
        print("INSTANTIATING OBJECT DETECTOR")
        objDetector = ObjectDetector("/home/cvard/Documents/project/ssdlite_mobilenet_v2_coco_2018_05_09/frozen_inference_graph.pb")
        print("STARTING TENSORFLOW SESSION")
        objDetector.startSession()
        while cv2.getWindowProperty(windowName, 0) >= 0: # if window isn't closed by user
            
            # read() returns bool (1: success, 0: fail) and frame
            ret, frame = vidCapObj.read()
            
            # allow frame it be modified in place
            frame.setflags(write=1)

            # format to np array: [1,None,None,3] so net is happy
            frame_formatted = np.expand_dims(frame, axis=0) 
        
            # run objection detection on input frame that has been formatted 
            boxes, scores, classes, num = objDetector.run(frame_formatted)
            
            # draw resulting boxes and classes on frame itself
            
            vis.draw_bounding_box_on_image(
                    image=frame,
                    ymin=boxes[0][0][0],
                    xmin=boxes[0][0][1],
                    ymax=boxes[0][0][2],
                    xmax=boxes[0][0][3],
                    color='red',
                    thickness=4,
                    display_str_list=['apple'],
                    use_normalized_coordinated=True)
            
            # display frame in specified window
            cv2.imshow(windowName, frame)

            # if user hits 'q' key, close window and exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            

if __name__ == "__main__":
    try:
        sys.path.append('../') 
        cap = openCamera() # get VideoCapture Object
        readFromCamera(cap) # capture and display frames
        cap.release() # close camera connection
        cv2.destroyAllWindows() # destory GUI window
    except:
        cap.release()
        cv2.destroyAllWindows()
        sys.exit(0)
