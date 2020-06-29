import numpy as np
import cv2
import sys

# create VideoCapture object and return it
def openCamera():
    return cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")


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
            print('in while loop') 
            # read() returns bool (1: success, 0: fail) and frame
            ret, frame = vidCapObj.read()
            
            # allow frame it be modified in place
            frame.setflags(write=1)

            # format to np array: [1,None,None,3] so net is happy
            frame_formatted = np.expand_dims(frame, axis=0) 
        
            # run objection detection on input frame that has been formatted 
            boxes, scores, classes, num = objDetector.run(frame_formatted)
            
            # draw resulting boxes and classes on frame itself
            #print(boxes)
            #print(scores)
            #print(classes)
            #print(classes)
            print('drawing')

            vis.draw_all_boxes_on_images(
                    image=frame,
                    boxes=np.atleast_2d(np.squeeze(boxes)),
                    classes=np.atleast_1d(np.squeeze(classes).astype(np.int32)),
                    scores=np.atleast_1d(np.squeeze(scores)))
            '''
            vis.draw_bounding_box_on_image(
                    image=frame,
                    ymin=0.27087304,
                    xmin=0.4052909,
                    ymax=0.99364685,
                    xmax=0.9999351,
                    color='red',
                    thickness=4,
                    display_str_list=['sample'],
                    use_normalized_coordinates=True)
            '''
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
