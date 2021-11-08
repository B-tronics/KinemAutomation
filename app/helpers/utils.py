import re
import cv2
import os
from helpers.log import createLogger
from helpers import globals

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

def setCoordinateOrder(psm):
    
    print(f"Add the following data for {psm} arm.")

    if psm == "left":
        # Get the user inputs
        globals.ORIGO_LEFT_PSM = int(input("Origo: "))
        globals.UPRIGHT_FROM_ORIGO_LEFT_PSM = int(input("Right from origo (upper): "))
        globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM = int(input("Right from origo (lower): "))
        globals.LEFT_FROM_ORIGO_LEFT_PSM = int(input("Left from origo: "))
        globals.ABOVE_ORIGO_LEFT_PSM = int(input("Above origo: "))
        globals.BELOW_ORIGO_LEFT_PSM = int(input("Below origo: "))
    elif psm == "right":
        # Get the user inputs
        globals.ORIGO_RIGHT_PSM = int(input("Origo: "))
        globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM = int(input("Right from origo (upper): "))
        globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM = int(input("Right from origo (lower): "))
        globals.LEFT_FROM_ORIGO_RIGHT_PSM = int(input("Left from origo: "))
        globals.ABOVE_ORIGO_RIGHT_PSM = int(input("Above origo: "))
        globals.BELOW_ORIGO_RIGHT_PSM = int(input("Below origo: "))

    else:
        logger.warning("Wrong psm name was introduced.")
        exit()

def createDBPath(databaseName):
    # Create the database path
    dir = os.path.expandvars("$APPDATA/KinemAutomation").replace('$APPDATA', os.path.expanduser('~/.config'))

    # Try to create the folder structure
    try:
        os.makedirs(dir, exist_ok=True)
    except:
        logger.error("Creation of the database folder has failed.")
        exit()

    logger.info("Creation of the database folder has been successful.")

    # Create the fulle path to the database
    filePath = os.path.join(dir, databaseName)
    
    return filePath