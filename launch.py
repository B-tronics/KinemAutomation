import argparse
from sqlite3.dbapi2 import Error
import subprocess
import pipes
import os
import sqlite3
import csv
import pandas as pd

def getNumberOfRows(file):
    num = 0
    for row in file:
        num += 1
    return num

def createConnection():
    conn = None
    
    try:
        conn = sqlite3.connect("KinemAutomation.db")
    except Error as e:
        print(e)
    
    return conn

def exportData(videoName, fileName):
    conn = createConnection()
    cursor = conn.cursor()

    idLeft = cursor.execute(f"SELECT id FROM video WHERE video_name = '{videoName}' AND psm_side = 'left'").fetchall()[0][0]
    idRight = cursor.execute(f"SELECT id FROM video WHERE video_name = '{videoName}' AND psm_side = 'right'").fetchall()[0][0]

    sqlLeft = f"SELECT psm_origo_x, psm_origo_y, psm_leftFromOrigo_x, psm_leftFromOrigo_y, psm_rightFromOrigoUp_x, psm_rightFromOrigoUp_y, psm_rightFromOrigoDown_x, psm_rightFromOrigoDown_y, psm_belowOrigo_x, psm_belowOrigo_y, psm_aboveOrigo_x, psm_aboveOrigo_y FROM kinematics2d WHERE video_name_id = {idLeft}"
    sqlRight = f"SELECT psm_origo_x, psm_origo_y, psm_leftFromOrigo_x, psm_leftFromOrigo_y, psm_rightFromOrigoUp_x, psm_rightFromOrigoUp_y, psm_rightFromOrigoDown_x, psm_rightFromOrigoDown_y, psm_belowOrigo_x, psm_belowOrigo_y, psm_aboveOrigo_x, psm_aboveOrigo_y FROM kinematics2d WHERE video_name_id = {idRight}"

    leftData = cursor.execute(sqlLeft).fetchall()
    rightData = cursor.execute(sqlRight).fetchall()
    filesPath = f"{os.getcwd()}/data/JIGSAWS/Knot_Tying/video/csvs/"

    leftFile = f"{filesPath}{fileName}_1.csv"
    rightFile = f"{filesPath}{fileName}_2.csv"

    if os.path.isfile(leftFile):
        os.remove(leftFile)
    if os.path.isfile(rightFile):
        os.remove(rightFile)

    with open(leftFile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(leftData)
    
    with open(rightFile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rightData)

    conn.close()

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--file", help="Rout to the file, containing the list of video file names.")
# args = vars(ap.parse_args())
args = {"file": "Knot_Tying.txt"}
with open(args["file"]) as f:
    numOfRows = getNumberOfRows(f) // 2

with open(args["file"]) as f:
    i = 0
    for name in f:
        i += 1
        vlPath = f"{os.getcwd()}/app/jigsaws/Knot_Tying/video/{name}"
        vrPath = f"{os.getcwd()}/app/jigsaws/Knot_Tying/video/{next(f)}"

        vlName = vlPath.split('/')[-1]
        tagsToRemove = vlName.split("_")[-1]
        videoName = vlName.replace(f"_{tagsToRemove}", "")
        tagsToRemove = videoName.split("_")[1]
        fileName = videoName.replace(f"_{tagsToRemove}", "")
        skillNum = (fileName.split("_")[1])
        skill = ''.join(i for i in skillNum if not i.isdigit())
        num = ''.join(i for i in skillNum if i.isdigit())
        fileName = fileName.replace(skillNum, f"{skill}_{num}")

        print(f"Construct data for {videoName}.")
        finished = False
        skip = input("Skip this file? Y/N: ")
        if skip == 'Y' or skip == 'y':
            print(f"Skipping file: {videoName}.\n")
            continue
        else:
            while not finished:
                print(f"Processing {i}/{numOfRows}\n")
                subprocess.run(["python3", "app/main.py", "-vl", pipes.quote(vlPath.strip('\n')), "-vr", pipes.quote(vrPath.strip('\n'))])
                answer = input("Is the process complete? Y/N: ")
                if answer == 'Y' or answer =='y':
                    exportData(videoName=videoName, fileName=fileName)
                    finished = True

