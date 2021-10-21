import cv2 as cv
import numpy as np

class PointSelector:
    def __init__(self, winName, maxNumberOfPoints):
        self.points = np.array([[]])
        self.name = winName
        self.pointsPrinted = 0
        self.selectPointsCalled = False
        self.allPointSelected = False
        self.maxNumberOfPoints = maxNumberOfPoints 

    def selectPoints(self, event, xCoordinate, yCoordinate, flags, params):
        
        # the sequence fires, when we give left mouse clicked event on the freezed frame
        # if all the points has been selected, we deny the selection, so new points will not be
        # accepted during the main sequence
        if event == cv.EVENT_LBUTTONDOWN and not self.allPointSelected:

            if not self.selectPointsCalled:
                # this is the first time the function has been called
                # create the numpy array with the selected coordinates
                self.points = np.array([[xCoordinate, yCoordinate]], dtype=np.float32)

                # change the function called status to true
                self.selectPointsCalled = True
            else:
                # self.point array is not empty
                # create a new numpy array with the current coordinates
                tempPoints = np.array([[xCoordinate, yCoordinate]], dtype=np.float32)

                # append the already existing numpy array with the new coordinates
                self.points = np.append(self.points, tempPoints, axis=0)

            # draw the coordinate points on the frame
            cv.circle(params, (xCoordinate, yCoordinate), 1, (0,255,0), -1)  

            # write the currently selected point's coordinate to the frame
            cv.putText(params, f"P{self.pointsPrinted + 1}: {self.points[0 + self.pointsPrinted]}", (10, 15 + (20 * self.pointsPrinted)), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            # give id to the selected point
            cv.putText(params, f"P{self.pointsPrinted + 1}", (xCoordinate - 10, yCoordinate - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # show the refreshed frame
            cv.imshow(self.name, params)

            # increase the number of points printed
            self.pointsPrinted += 1
            
            # check if we have selected the maximum number of points
            if len(self.points) == self.maxNumberOfPoints:
                self.allPointSelected = True