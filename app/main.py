 # <<<<<<< PREPARATION >>>>>>>>>

import argparse
from helpers import log
import os
from helpers import globals

# get the base directory name
globals.BASEDIR = os.getcwd() + "/app"
# create argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-vl", "--video_left", required=True, help="Path to the left video file.")
ap.add_argument("-vr", "--video_right", required=True, help="Path to the right video file.")
ap.add_argument("-c", "--config", required=False, default=f"{globals.BASEDIR}/config.json", help="Path to the config file.")
args = vars(ap.parse_args())

# get the configuration values
from helpers.config import getConfig
from helpers.utils import createDBPath
confData = getConfig(args["config"])


# set global variables
globals.LOGFILENAME = confData["LOGFILENAME"]
globals.TEMPLATENAME = confData["TEMPLATENAME"]
globals.JIGSAWSPATH = confData["JIGSAWSPATH"]
globals.PNPNUMBER = confData["PNPNUMBER"]
globals.DBNAME = createDBPath(confData["DATABASENAME"])

# create video table video_name field
videoFileName = (args["video_left"].split("/")[-1])
tagsToRemove = videoFileName.split("_")[-1]
videoName = videoFileName.replace(f"_{tagsToRemove}", "")

# delete the existing log file
if os.path.exists(globals.LOGFILENAME):
    os.remove(globals.LOGFILENAME)

# import the neccessary modules
import cv2 as cv
import numpy as np
from helpers.log import createLogger
from helpers.pointselector import PointSelector

# <<<<<<< PREPARATION >>>>>>>>>

# <<<<<<< INITIALIZATION >>>>>>>>>

# create the module logger
logger = createLogger(__name__, globals.LOGFILENAME)

# import database related modules
from database.jigsawsdata import readData
from helpers.utils import getFileName
from poseestimation.pnp import get3DCoordinates

# get the matching points
from featurepoints.featurepoints import detectMatchingPoints
matchingPoints = detectMatchingPoints(args["video_left"], args["video_right"])

# create the database and import the models
from database.db import db
if db is not None:
    logger.info("Database has been created.")

from database.model import createTables, populateKinematicTable, populateVideoTable
# Create the database tables
createTables()

# Populate the database with the current videofile name
populateVideoTable(videoName)

# get the jigsaws kinematic data for the current video
jigsawsData = readData(globals.JIGSAWSPATH, getFileName(os.path.basename(args["video_left"])))

# create video-object
videoObj = cv.VideoCapture(args["video_right"])

# grab the first frame
frame = videoObj.read()[1]

# create the window to show
winName = "Video"
cv.namedWindow(winname=winName)

# initialize the pointSelector object and set the mouse callback function
pointSelector = PointSelector(points=matchingPoints)
cv.setMouseCallback(winName, pointSelector.selectPoints, matchingPoints)

# transform the first frame to gray 
grayFrameOld = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Lucas Kanade parameters
lkParams = dict(winSize=(17, 17), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# <<<<<<< INITIALIZATION >>>>>>>>>


def main(frame=frame, grayFrameOld = grayFrameOld):

    # <<<<<<< PRE-PROCESSING >>>>>>>>>
    frameCopy = frame.copy()
    # select the points for PNP estimation
    cv.imshow(winName, frame)
    while True:

        # draw the coordinate points on the frame
        # TODO: traverse the pointSelector._pointsOrder dictionary.
        for i, point in enumerate(pointSelector._pointsOrder):
            # TODO: give comments to these lines
            cv.circle(frame, (int(pointSelector._pointsOrder[point][0]), int(pointSelector._pointsOrder[point][1])), 5, (0,255,0), -1)
            cv.putText(frame, f"{point} : {(pointSelector._pointsOrder[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            cv.putText(frame, f"{point}", (int(pointSelector._pointsOrder[point][0]-10), int(pointSelector._pointsOrder[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # show the refreshed frame
        cv.imshow(winName, frame)
        key = cv.waitKey(1)
        if key == 27:
            break
        frame = frameCopy.copy()
    logger.info("All points has been specified.")

    from helpers.utils import setCoordinateOrder
    # Set the coordinate order
    setCoordinateOrder("left")
    setCoordinateOrder("right")
    # the frame now starts to move
    pointSelector._frameMoving = True

    # initialize frame count
    FRAMECOUNT = 0

    # <<<<<<< PRE-PROCESSING >>>>>>>>>

    # <<<<<<<<<< MAIN LOOP >>>>>>>>>>>

    while True:
        # grab the next frame
        frame = videoObj.read()[1]

        # increase the frame count
        FRAMECOUNT += 1

        # if we can not grab the current frame, we are at the end of the video
        if frame is None:
            logger.info("Processing of video files has been finished.")
            break
        
        # transform the current frame to gray
        grayFrameNew = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # track the selected points
        newPoints, status, error = cv.calcOpticalFlowPyrLK(grayFrameOld, grayFrameNew, pointSelector._points, None, **lkParams)
        """
        if not BaseDB.tablesCreated:
            BaseDB.createTables(BaseDB, model=models.TestDbKinematics)

        if DATABASENAME != "diplomamunka.sqite":
            data = models.TestDbKinematics(
                                    P1_x_coordinate=newPoints[0][0], 
                                    P1_y_coordinate=newPoints[0][1],
                                    P2_x_coordinate=newPoints[1][0],
                                    P2_y_coordinate=newPoints[1][1],
                                    P3_x_coordinate=newPoints[2][0],
                                    P3_y_coordinate=newPoints[2][1],
                                    P4_x_coordinate=newPoints[3][0],
                                    P4_y_coordinate=newPoints[3][1],
                                    P5_x_coordinate=newPoints[4][0],
                                    P5_y_coordinate=newPoints[4][1],
                                    P6_x_coordinate=newPoints[5][0],
                                    P6_y_coordinate=newPoints[5][1]
            )
            try:       
                data.save()
            except:
                logger.warning(f"Kinematic data for frame: {FRAMECOUNT}, has failed!")

            logger.info(f"Kinematic data for frame: {FRAMECOUNT}, was successfull.")
            """
        # copy the newPoints to the old points
        grayFrameOld = grayFrameNew
       
        # write the original points over with the new points
        pointSelector._points = newPoints
        for i, key in enumerate(pointSelector._pointsOrder):
            pointSelector._pointsOrder[key] = newPoints[i]

        # update the labels
        for i, point in enumerate(pointSelector._pointsOrder):
            # TODO: give comments to these lines
            cv.circle(frame, (int(pointSelector._pointsOrder[point][0]), int(pointSelector._pointsOrder[point][1])), 5, (0,255,0), -1)
            cv.putText(frame, f"{point} : {(pointSelector._pointsOrder[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            cv.putText(frame, f"{point}", (int(pointSelector._pointsOrder[point][0]-10), int(pointSelector._pointsOrder[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        
        # get the 3D coordinates
        # TODO
        left3D = get3DCoordinates(pointSelector._points, "left", frame)
        right3D = get3DCoordinates(pointSelector._points, "right", frame)

        # show the current frame
        cv.imshow(winName, frame)        
        key = cv.waitKey(1) & 0xFF

        # if 'q' key was pressed, break the loop
        if key == ord('q'):
            logger.warning("Processing of the video files has been interrupted.")
            break
        if key == ord('p'):
            while True:
                pointSelector._frameMoving = False

                for i, point in enumerate(pointSelector._pointsOrder):
                    # TODO: give comments to these lines
                    cv.circle(frame, (int(pointSelector._pointsOrder[point][0]), int(pointSelector._pointsOrder[point][1])), 5, (0,255,0), -1)
                    cv.putText(frame, f"{point} : {(pointSelector._pointsOrder[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                    cv.putText(frame, f"{point}", (int(pointSelector._pointsOrder[point][0]-10), int(pointSelector._pointsOrder[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                cv.imshow(winName, frame)
                
                key_p = cv.waitKey(1)
                if key_p == ord('q'):
                    pointSelector._frameMoving = True
                    break
                frame = frameCopy.copy()
    db.close()
    # <<<<<<<<<< MAIN LOOP >>>>>>>>>>>

if __name__ == "__main__":
    main()

