from operator import le
from re import S
import cv2 as cv
import numpy as np
import math

from helpers.globals import POINTSORDER
class PointSelector:
    def __init__(self, points):
        self._points = points
        self._frameMoving = False
        self._pointsOrder = {}
        self._pointNumber = points.shape[0] + 1
        self._movePoint = False
        self._pointToMove = -1
        # initialize dict
        for i, value in enumerate(points):
            self._pointsOrder[i + 1] = value

    def selectPoints(self, event, xCoordinate, yCoordinate, flags, params):
        # select points (available only if the frame is standstill)
        if event == cv.EVENT_LBUTTONDOWN and not self._frameMoving:
            if not self._movePoint:
                self._pointsOrder[self._pointNumber] = (xCoordinate, yCoordinate)
                self._pointNumber += 1
            else:
                self._pointsOrder[self._pointToMove] = (xCoordinate, yCoordinate)
                self._movePoint = False 
        
            # update the points list
            self._points = np.zeros((len(self._pointsOrder), 2), dtype=np.float32)
            for i, key in enumerate(self._pointsOrder):
                self._points[i] = self._pointsOrder[key]

        # delete a point from the list
        if event == cv.EVENT_RBUTTONDOWN and not self._frameMoving:
            diff = {}
            for point in self._pointsOrder:
                xd = math.pow((self._pointsOrder[point][0] - xCoordinate), 2)
                yd = math.pow((self._pointsOrder[point][1] - yCoordinate), 2)
                d = math.sqrt(xd + yd)
                diff[point] = d
            diffKeys = list(diff.keys())
            diffValues = list(diff.values())
            valueToDelete = diffValues.index(min(diffValues))
            pointToDelete = diffKeys[valueToDelete]
            self._pointsOrder.pop(pointToDelete)
            self._pointToMove = pointToDelete
            self._movePoint = True

            # update the points list
            self._points = np.zeros((len(self._pointsOrder), 2), dtype=np.float32)
            for i, key in enumerate(self._pointsOrder):
                self._points[i] = self._pointsOrder[key]
        