import cv2
import numpy as np


def drawFeaturePoints(videoLeft, videoRight):
    matchingImage = detectKeyPoints(videoLeft, videoRight)
    cv2.imwrite("matches.jpg", matchingImage)

def detectKeyPoints(videoLeft, videoRight):

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
    # TODO: Filter the matches
    pointsLeft = filterPoints(roiLeft, pointsLeft)
    pointsRight = filterPoints(roiRight, pointsRight)

    matchingImage = cv2.drawMatchesKnn(imageLeft, keyPointsLeft, imageRight, keyPointsRight, matches[:300], None)
    for point in pointsRight:
        cv2.circle(imageLeft, tuple(point), 5, 200, -1)
    for point in pointsLeft:
        cv2.circle(imageLeft, tuple(point), 5, 200, -1)
    cv2.imshow("Left", imageLeft)
    cv2.waitKey(0)
    return matchingImage

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
    
    videoName = name + '.jpg'
    # read the first frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(videoName, frame)
    else:
        cap.release()
        cv2.destroyAllWindows()
        return None

    cap.release()
    cv2.destroyAllWindows()

    return videoName


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

drawFeaturePoints("/home/balint/Projects/KinemAuotomation/app/jigsaws/Knot_Tying/video/Knot_Tying_B001_capture1.avi", "/home/balint/Projects/KinemAuotomation/app/jigsaws/Knot_Tying/video/Knot_Tying_B001_capture2.avi")