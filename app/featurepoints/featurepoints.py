from operator import le
import cv2
import numpy as np 
from helpers.utils import getFirstFrame
from helpers.pointdeletion import PointFilter

def drawFeaturePoints(videoLeft, videoRight):

    # detect all the matching points
    points = detectMatchingPoints(videoLeft, videoRight)

    # create the filter event handler object
    pointFilter = PointFilter(points)

    # create the window to show
    winName = "Frame"
    cv2.namedWindow(winName)

    # register the mouse callback function
    cv2.setMouseCallback(winName, pointFilter.deletePoints)

    # read the first frame
    cap = cv2.VideoCapture(videoLeft)
    frame = cap.read()[1]
    frameCopy = frame.copy()

    # draw the keypoints on the first frame
    for point in points:
        cv2.circle(frame, tuple(point), 5, (0,255,0), -1)
    
    # delete all the unnecessary points
    while True:
        # update the points list
        points = pointFilter._points

        # draw the keypoints on the frame
        for point in points:
            cv2.circle(frame, tuple(point), 5, (0,255,0), -1)

        # make titles for the commands
        cv2.putText(frame, "(ESC) to continue.", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        cv2.putText(frame, "(Right mouse click) delete point", (30,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        # show the picture
        cv2.imshow(winName, frame)

        # capture the inputs
        key = cv2.waitKey(1)
        if key == 27:
            break

        # refresh the image
        frame = frameCopy.copy()

    # destroy the windows
    cap.release()
    cv2.destroyWindow(winName)

    # return the filtered list of points
    return points

def detectMatchingPoints(videoLeft, videoRight):

    # grab the first frames
    firstFrameLeft = getFirstFrame(videoLeft, "left")
    firstFrameRight = getFirstFrame(videoRight, "right")

    # read the frames as images
    imageLeft = cv2.imread(firstFrameLeft, 0)
    imageRight = cv2.imread(firstFrameRight, 0)

    # Create the SIFT detector and descriptor
    sift = cv2.SIFT_create()

    # Find the keypoints and descriptors with SIFT
    keyPointsLeft, descriptorLeft = sift.detectAndCompute(imageLeft,None)
    keyPointsRight, descriptorRigth = sift.detectAndCompute(imageRight,None)

    # FLANN matcher parameters
    FLANN_INDEX_KDTREE = 1
    INDEX_PARAMS = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    SEARCH_PARAMS = dict(checks=50)

    # Create the FLANN based matcher object, used to get all the matching keypoints of the two images
    flann = cv2.FlannBasedMatcher(INDEX_PARAMS, SEARCH_PARAMS)
    matches = flann.knnMatch(descriptorLeft, descriptorRigth, k=2)

    # Create two lists for the matches which are above a certain 'goodness' threshold (based on eucledian distance)
    pointsLeft = []
    pointsRight = []

    # Ratio test as per Lowe's paper, append the good points to the previously defined lists
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            pointsRight.append(keyPointsRight[m.trainIdx].pt)
            pointsLeft.append(keyPointsLeft[m.queryIdx].pt)

    # Convert the points to int32, so that correct pixel values can be gathered
    pointsLeft = np.int32(pointsLeft)
    pointsRight = np.int32(pointsRight)

    # Select the ROI for filtering the matching results (returns: x, y, width, height)
    roiLeft = cv2.selectROI(imageLeft)
    roiRight = cv2.selectROI(imageRight)
    # Filter the matches
    pointsLeft = filterPoints(roiLeft, pointsLeft)
    pointsRight = filterPoints(roiRight, pointsRight)

    cv2.destroyAllWindows()

    # Create the list of feature points
    points = np.zeros((len(pointsLeft) + len(pointsRight), 2), dtype=np.float32)
    i  = 0
    for point in pointsLeft:
        points[i] = point
        i += 1
    for point in pointsRight:
        points[i] = point
        i += 1
    return points


def filterPoints(roi, points):
    xRange = (roi[0], roi[0] + roi[2])
    yRange = (roi[1], roi[1] + roi[3])
    i = 0
    while points.shape[0] > i:
        if not ((points[i][0] >= xRange[0] and points[i][0] <= xRange[1]) and (points[i][1] >= yRange[0] and points[i][1] <= yRange[1])):
            points = np.delete(points, i, 0)
        else:
            i += 1
    return points