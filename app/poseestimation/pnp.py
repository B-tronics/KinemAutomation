import re
import cv2
import numpy as np
from helpers import globals

def get3DCoordinates(pointsList, frame, psm):

    size = frame.shape

    if psm == "left":
        # 2D image points
        imagePoints = np.array([
            (pointsList[globals.ORIGO_LEFT_PSM][0], pointsList[globals.ORIGO_LEFT_PSM][1]),                                   # Origo
            (pointsList[globals.UPRIGHT_FROM_ORIGO_LEFT_PSM][0], pointsList[globals.UPRIGHT_FROM_ORIGO_LEFT_PSM][1]),         # Right upper from origo
            (pointsList[globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM][0], pointsList[globals.DOWNRIGHT_FROM_ORIGO_LEFT_PSM][1]),     # Right lower from origo
            (pointsList[globals.LEFT_FROM_ORIGO_LEFT_PSM][0], pointsList[globals.LEFT_FROM_ORIGO_LEFT_PSM][1]),               # Left from origo
            (pointsList[globals.ABOVE_ORIGO_LEFT_PSM][0], pointsList[globals.ABOVE_ORIGO_LEFT_PSM][1]),                       # Above origo
            (pointsList[globals.BELOW_ORIGO_LEFT_PSM][0], pointsList[globals.BELOW_ORIGO_LEFT_PSM][1])                        # Below origo
        ])
    else:
        # 2D image points
        imagePoints = np.array([
            (pointsList[globals.ORIGO_RIGHT_PSM][0], pointsList[globals.ORIGO_RIGHT_PSM][1]),                                   # Origo
            (pointsList[globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM][0], pointsList[globals.UPRIGHT_FROM_ORIGO_RIGHT_PSM][1]),         # Right upper from origo
            (pointsList[globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM][0], pointsList[globals.DOWNRIGHT_FROM_ORIGO_RIGHT_PSM][1]),     # Right lower from origo
            (pointsList[globals.LEFT_FROM_ORIGO_RIGHT_PSM][0], pointsList[globals.LEFT_FROM_ORIGO_RIGHT_PSM][1]),               # Left from origo
            (pointsList[globals.ABOVE_ORIGO_RIGHT_PSM][0], pointsList[globals.ABOVE_ORIGO_RIGHT_PSM][1]),                       # Above origo
            (pointsList[globals.BELOW_ORIGO_RIGHT_PSM][0], pointsList[globals.BELOW_ORIGO_RIGHT_PSM][1])                        # Below origo
        ])

    # declare the 2d variables for convinience
    origo = (imagePoints[0][0], imagePoints[0][1])
    rightUpper = (imagePoints[1][0], imagePoints[1][1])
    rightLower = (imagePoints[2][0], imagePoints[2][1])
    left = (imagePoints[3][0], imagePoints[3][1])
    up = (imagePoints[4][0], imagePoints[4][1])
    down = (imagePoints[5][0], imagePoints[5][1])

    # to convert the mm values given, we will use the following formula:
    # 1px = 1inch / dpi where the dpi value is know from the video metadata and the inch is equal to 25.4mm
    dpi = 96    
    inch = 25.4
    # 3D model points
    # TODO: finish the matrix
    realOrigo = (0.0, 0.0, 0.0)
    realRightUpper = ()
    realRightLower = ()
    realLeft = ()
    realUp = (0.0, ((-0.124*inch)/dpi), )
    realDown = ()

    modelPoints = np.array([
        realOrigo,
        realRightUpper,
        realRightLower,
        realLeft,
        realUp,
        realDown
    ])

    # define the camera internals
    focalLength = size[1]
    center = (size[1]/2, size[0]/2)
    cameraMatrix = np.array(
        [[focalLength, 0, center[0]],
        [0, focalLength, center[1]],
        [0, 0, 1]], dtype="double"
    )

    # Ignore the lens distortiotion
    distCoeffs = np.zeros((4,1))
    (success, rotationVector, translationVector) = cv2.solvePnP(modelPoints, imagePoints, cameraMatrix, distCoeffs, flags=cv2.CV_ITERATIVE)
    return 0