import cv2
import math


POINTS = []

class PointFilter:
    def __init__(self, points):
        self._points = points

    def deletePoints(self, event, xCoordinate, yCoordinate, flags, params):
        if event == cv2.EVENT_RBUTTONDOWN:
            diff = list()
            for point in self._points:
                xd = math.pow((point[0] - xCoordinate), 2)
                yd = math.pow((point[1] - yCoordinate), 2)
                d = math.sqrt(xd + yd)
                diff.append(d)
            pointToDelete = diff.index(min(diff))
            self._points.pop(pointToDelete)