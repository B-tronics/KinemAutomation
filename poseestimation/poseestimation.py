import cv2
import numpy as np
import argparse
import csv
import os
import glob

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--csv", help="Path to the CSV file holding the 2D data for the video.")
ap.add_argument("-v", "--video", help="Path to the video file.")
args = vars(ap.parse_args())

dir_name = args["csv"]
csv_list = [os.path.basename(x) for x in glob.glob(dir_name+"*.csv")]
csv_list.sort()

output_path = os.getcwd() + "/data/Knot_Tying/"
try:
    os.makedirs(output_path)
except FileExistsError as e:
    pass

dir_name = args["video"]
video_list = [os.path.basename(x) for x in glob.glob(dir_name+"*.avi")]
video_list.sort()

for i, csvs_file in enumerate(csv_list):

    video_path = args["video"] + video_list[i]
    cap = cv2.VideoCapture(video_path)
    frame = cap.read()[1]
    frameSize = frame.shape
    cap.release()

    rows = []
    
    result_file = output_path + csvs_file
    csv_file_path = args["csv"] + csvs_file

    with open(csv_file_path, "r") as f:
        csvReader = csv.reader(f)
        
        for i, row in enumerate(csvReader):
            rows.append(list(row))

    modelPoints = np.array([
            (0.0, 0.0, 0.0),    # Origo
            (2.0, 0.0, 2.8),    # Left from Origo 
            (10.83, 0.5, 0.5),  # RightAbove from Origo
            (10.83, -0.5, 0.5), # RightBelow from Origo
            (0.0, -3.16, 0.5),  # Below Origo
            (0.0, 3.16, 0.5)    # Above Orgio
    ])

    focalLength = frameSize[1]
    center = (frameSize[1]/2, frameSize[0]/2)
    cameraMatrix = np.array([
        [focalLength, 0, center[0]],
        [0, focalLength, center[1]],
        [0,0,1]
    ], dtype="double")

    distCoeffs = np.zeros((4,1))

    with open(result_file, 'w') as r:
            rwriter = csv.writer(r)
            for row in rows:
                imagePoints = np.array([
                    (float(row[0]), float(row[1])),                             # Origo
                    (float(row[2]), float(row[3])),             # Left from Origo
                    (float(row[4]), float(row[5])),       # RightAbove from Origo
                    (float(row[6]), float(row[7])),   # RightBelow from Origo
                    (float(row[8]), float(row[9])),                   # Below Origo
                    (float(row[10]), float(row[11]))                    # Above Origo
                ])

                (success, rotationVector, translationVector) = cv2.solvePnP(
                                                                            modelPoints, 
                                                                            imagePoints,
                                                                            cameraMatrix,
                                                                            distCoeffs,
                                                                            flags=cv2.SOLVEPNP_ITERATIVE)

                data = [translationVector[0][0], translationVector[1][0], translationVector[2][0]]
                rwriter.writerow(data)