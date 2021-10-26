import re
import cv2
import os
from helpers.log import createLogger

# TODO: add logging to this module

logger = createLogger(__name__, "app.log")

def getFileName(path):
    file_name = re.sub("\_capture..avi$", "", path)
    return file_name

def getFirstFrame(video, name):
    """
    The function saves the video file's first frame in the current folder.
        Params:
            video (string): Path to the video file
            name (string): Name of the new image
        Returns:
            name (string): name of the created image
    """
    #Open the videofile
    cap = cv2.VideoCapture(video)
    
    frameName = os.getcwd() + "/" + name + '.jpg'
    # read the first frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(frameName, frame)
    else:
        cap.release()
        cv2.destroyAllWindows()
        return None

    cap.release()
    cv2.destroyAllWindows()

    return frameName