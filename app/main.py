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
globals.DBNAME = confData["DATABASENAME"]

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
# from poseestimation.pnp import get3DTransformationData

# get the matching points
from featurepoints.featurepoints import detectMatchingPoints
matchingPoints = detectMatchingPoints(args["video_left"], args["video_right"])

# create the database and import the models
from database.db import db
if db is not None:
    logger.info("Database has been created.")

from database.model import createTables, deleteExistingVideoRows, populateVideoTable, getVideoId, deleteExistingKinematicRows, populateKinematic2DTable
# Create the database tables
createTables()

# Check if instance data for the current video file already exists, and if so, delete it so always the fresh data is used.
execDelRight = deleteExistingKinematicRows(videoName, 'right')
execDelLeft = deleteExistingKinematicRows(videoName, 'left')
if execDelRight is not None:    
    db.execute(execDelRight)
if execDelLeft is not None:
    db.execute(execDelLeft)
db.execute(deleteExistingVideoRows(videoName))

# Populate the video table
populateVideoTable(videoName)

# get the videoIds for populating the kinematic tables
leftVideoId, rightVideoId = getVideoId(videoName)
# get the jigsaws kinematic data for the current video
jigsawsData = readData(globals.JIGSAWSPATH, getFileName(os.path.basename(args["video_left"])))

# create video-object
videoObj = cv.VideoCapture(args["video_right"])

# grab the first frame
frame = videoObj.read()[1]

# create the window to show
winName = "Video"
cv.namedWindow(winName, cv.WINDOW_NORMAL)
cv.resizeWindow(winName, 1280, 768)

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
        for i, point in enumerate(pointSelector._pointsOrder):
            # TODO: give comments to these lines
            cv.circle(frame, (int(pointSelector._pointsOrder[point][0]), int(pointSelector._pointsOrder[point][1])), 2, (0,255,0), -1)
            cv.putText(frame, f"{point} : {(pointSelector._pointsOrder[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 2)
            cv.putText(frame, f"{point}", (int(pointSelector._pointsOrder[point][0]-10), int(pointSelector._pointsOrder[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 2)

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

    # initialize frame count
    FRAMECOUNT = 0

    globals.POSITIONSLIST = [
        globals.ORIGO_LEFT_PSM,
        globals.UPRIGHT_FROM_ORIGO_LEFT_PSM,
        globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM,
        globals.LEFT_FROM_ORIGO_LEFT_PSM,
        globals.ABOVE_ORIGO_LEFT_PSM,
        globals.BELOW_ORIGO_LEFT_PSM,
        globals.ORIGO_RIGHT_PSM,
        globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM,
        globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM,
        globals.LEFT_FROM_ORIGO_RIGHT_PSM,
        globals.ABOVE_ORIGO_RIGHT_PSM,
        globals.BELOW_ORIGO_RIGHT_PSM
    ]

    # <<<<<<< PRE-PROCESSING >>>>>>>>>

    # <<<<<<<<<< MAIN LOOP >>>>>>>>>>>

    while True:
        # update the kinematic data dictionary
        globals.POINTSORDER = {
        "ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.ORIGO_LEFT_PSM],
        "UPRIGHT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.UPRIGHT_FROM_ORIGO_LEFT_PSM],
        "DOWNRIGHT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM],
        "LEFT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.LEFT_FROM_ORIGO_LEFT_PSM],
        "ABOVE_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.ABOVE_ORIGO_LEFT_PSM],
        "BELOW_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.BELOW_ORIGO_LEFT_PSM],
        "ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.ORIGO_RIGHT_PSM],
        "UPRIGHT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM],
        "DOWNRIGHT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM],
        "LEFT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.LEFT_FROM_ORIGO_RIGHT_PSM],
        "ABOVE_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.ABOVE_ORIGO_RIGHT_PSM],
        "BELOW_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.BELOW_ORIGO_RIGHT_PSM]
    }
        # grab the next frame
        frame = videoObj.read()[1]

        # wait for the start signal
        if not pointSelector._frameMoving:
            frameCopy = frame.copy()
            while True:
                # draw the coordinate points on the frame
                for i, point in enumerate(globals.POINTSORDER):
                    # TODO: give comments to these lines
                    cv.circle(frame, (int(globals.POINTSORDER[point][0]), int(globals.POINTSORDER[point][1])), 2, (0,255,0), -1)
                    cv.putText(frame, f"{point} : {(globals.POINTSORDER[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 2)
                    cv.putText(frame, f"{point}", (int(globals.POINTSORDER[point][0]-10), int(globals.POINTSORDER[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0), 2)

                # show the refreshed frame
                cv.imshow(winName, frame)
                key = cv.waitKey(1)
                if key == ord('a'):
                    # the frame now starts to move
                    pointSelector._frameMoving = True
                    break
                frame = frameCopy.copy()

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

        # copy the newPoints to the old points
        grayFrameOld = grayFrameNew
       
        # write the original points over with the new points
        pointSelector._points = newPoints
        for i, key in enumerate(pointSelector._pointsOrder):
            pointSelector._pointsOrder[key] = newPoints[i]

        # update the labels
        for i, point in enumerate(globals.POINTSORDER):
            # TODO: give comments to these lines
            cv.circle(frame, (int(globals.POINTSORDER[point][0]), int(globals.POINTSORDER[point][1])), 5, (0,255,0), -1)
            #cv.putText(frame, f"{point} : {(globals.POINTSORDER[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
            #cv.putText(frame, f"{point}", (int(pointSelector._pointsOrder[point][0]-10), int(pointSelector._pointsOrder[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        
        # get the 3D coordinates
        # TODO
        # left3D = get3DTransformationData(pointSelector._points, "left", frame)
        # right3D = get3DTransformationData(pointSelector._points, "right", frame)

        # Save the Kinematic data for the right video_name
        populateKinematic2DTable(globals.POINTSORDER, videoName, "left")
        populateKinematic2DTable(globals.POINTSORDER, videoName, "right")
        # show the current frame
        cv.imshow(winName, frame)        
        key = cv.waitKey(500) & 0xFF

        # if 'q' key was pressed, break the loop
        if key == ord('q'):
            logger.warning("Processing of the video files has been interrupted.")
            break
        if key == ord('p'):
            frameCopy = videoObj.read()[1]

            while True:
                if not pointSelector._movePoint:
                    globals.POINTSORDER = {
                        "ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.ORIGO_LEFT_PSM],
                        "UPRIGHT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.UPRIGHT_FROM_ORIGO_LEFT_PSM ],
                        "DOWNRIGHT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM],
                        "LEFT_FROM_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.LEFT_FROM_ORIGO_LEFT_PSM],
                        "ABOVE_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.ABOVE_ORIGO_LEFT_PSM],
                        "BELOW_ORIGO_LEFT_PSM": pointSelector._pointsOrder[globals.BELOW_ORIGO_LEFT_PSM],
                        "ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.ORIGO_RIGHT_PSM],
                        "UPRIGHT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM],
                        "DOWNRIGHT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM],
                        "LEFT_FROM_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.LEFT_FROM_ORIGO_RIGHT_PSM],
                        "ABOVE_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.ABOVE_ORIGO_RIGHT_PSM],
                        "BELOW_ORIGO_RIGHT_PSM": pointSelector._pointsOrder[globals.BELOW_ORIGO_RIGHT_PSM]
                    }
                pointSelector._frameMoving = False

                for i, point in enumerate(globals.POINTSORDER):
                    # TODO: give comments to these lines
                    cv.circle(frame, (int(globals.POINTSORDER[point][0]), int(globals.POINTSORDER[point][1])), 5, (0,255,0), -1)
                    cv.putText(frame, f"{point} : {(globals.POINTSORDER[point])}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                    #cv.putText(frame, f"{point}", (int(globals.POINTSORDER[point][0]-10), int(globals.POINTSORDER[point][1]-10)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

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

