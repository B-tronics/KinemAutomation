 # <<<<<<< PREPARATION >>>>>>>>>

import argparse
from helpers import log
# create argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-vl", "--video_left", required=True, help="Path to the left video file.")
ap.add_argument("-vr", "--video_right", required=True, help="Path to the right video file.")
ap.add_argument("-c", "--config", required=False, default="/home/balint/Projects/KinemAuotomation/app/config.json", help="Path to the config file.")
args = vars(ap.parse_args())

# get the configuration values
from helpers.config import getConfig
confData = getConfig(args["config"])

# set global variables
LOGFILENAME = confData["LOGFILENAME"]
TEMPLATENAME = confData["TEMPLATENAME"]
DATABASENAME = confData["DATABASENAME"]
JIGSAWSPATH = confData["JIGSAWSPATH"]
PNPNUMBER = confData["PNPNUMBER"]

import os
# delete the existing log file
if os.path.exists(LOGFILENAME):
    os.remove(LOGFILENAME)

# import the neccessary modules
import cv2 as cv
import numpy as np
from helpers.log import createLogger
from helpers.pointselector import PointSelector

# <<<<<<< PREPARATION >>>>>>>>>

# <<<<<<< INITIALIZATION >>>>>>>>>

# create the module logger
logger = createLogger(__name__, LOGFILENAME)

# import database related modules
from database.db import BaseDB
from database.jigsawsdata import readData
from helpers.getfilename import getFileName

# create the database and import the models
db = BaseDB(DATABASENAME, TEMPLATENAME).db
if db is not None:
    logger.info("Database has been created.")

# import database model
from database import models
 
# get the jigsaws kinematic data for the current video
jigsawsData = readData(JIGSAWSPATH, getFileName(os.path.basename(args["video_left"])))

# create video-object
videoObj = cv.VideoCapture(args["video_left"])

# grab the first frame
frame = videoObj.read()[1]

# create the window to show
winName = "Video"
cv.namedWindow(winname=winName)

# initialize the pointSelector object and set the mouse callback function
pointSelector = PointSelector(winName=winName, maxNumberOfPoints=PNPNUMBER)
cv.setMouseCallback(winName, pointSelector.selectPoints, frame)

# transform the first frame to gray 
grayFrameOld = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

# Lucas Kanade parameters
lkParams = dict(winSize=(17, 17), maxLevel=2, criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

# <<<<<<< INITIALIZATION >>>>>>>>>


def main(frame=frame, grayFrameOld = grayFrameOld):

    # <<<<<<< PRE-PROCESSING >>>>>>>>>

    # select the points for PNP estimation
    cv.imshow(winName, frame)
    while not pointSelector.allPointSelected:
        cv.waitKey(1)
    logger.info("All points has been specified.")

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
        newPoints, status, error = cv.calcOpticalFlowPyrLK(grayFrameOld, grayFrameNew, pointSelector.points, None, **lkParams)

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

        # copy the newPoints to the old points
        grayFrameOld = grayFrameNew

        # draw the points to the frame
        for index, points in enumerate(newPoints):
            # update the points
            x = int(points[0])
            y = int(points[1])
            cv.circle(frame, (x, y), 5, (0,255,0), -1)

            # label the coordinates
            cv.putText(frame, f"P{index + 1}", (x - 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # write the original points over with the new points
        pointSelector.points = newPoints

        # put the points label to the frame
        for i in range(len(pointSelector.points)):
            cv.putText(frame, f"P{i + 1}: {pointSelector.points[0 + i]}", (10, 15 + (20 * i)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            

        # show the current frame
        cv.imshow(winName, frame)        
        key = cv.waitKey(1) & 0xFF

        # if 'q' key was pressed, break the loop
        if key == ord('q'):
            logger.warning("Processing of the video files has been interrupted.")
            break

    db.close()
    # <<<<<<<<<< MAIN LOOP >>>>>>>>>>>

if __name__ == "__main__":
    main()