import datetime
from peewee import *
from .db import db
from helpers.log import createLogger

# Invoke the logger
logger = createLogger(__name__, "app.log")


class BaseModel(Model):
    class Meta:
        database = db

class Video(BaseModel):
    video_name = TextField()
    psm_side = TextField()

class Kinematics2D(BaseModel):
    video_name = ForeignKeyField(Video, backref='kinematics2D', on_delete='CASCADE')
    frame = IntegerField()
    psm_origo_x = FloatField()
    psm_origo_y = FloatField()
    psm_leftFromOrigo_x = FloatField()
    psm_leftFromOrigo_y = FloatField()
    psm_rightFromOrigoUp_x = FloatField()
    psm_rightFromOrigoUp_y = FloatField()
    psm_rightFromOrigoDown_x = FloatField()
    psm_rightFromOrigoDown_y = FloatField()
    psm_belowOrigo_x = FloatField()
    psm_belowOrigo_y = FloatField()
    psm_aboveOrigo_x = FloatField()
    psm_aboveOrigo_y = FloatField()
class Kinematics(BaseModel):
    video_name = ForeignKeyField(Video)
    frame = IntegerField()
    psm_left_pos_x = FloatField()
    psm_left_pos_y = FloatField()
    psm_left_pos_z = FloatField()
    psm_right_pos_x = FloatField()
    psm_right_pos_y = FloatField()
    psm_right_pos_z = FloatField()

def createTables(Dim2=True):
    if not Dim2:
        try:
            db.connect()
        except:
            logger.warning("Connecting to the database has failed.")
            exit()
        try:
            db.create_tables([Video, Kinematics])
        except:
            logger.warning("Creating the tables has failed.")
    
    else:
        try:
            db.connect()
        except:
            logger.warning("Connecting to the database has failed.")
            exit()
        try:
            db.create_tables([Video, Kinematics2D])
        except:
            logger.warning("Creating the tables has failed.")

    logger.info("Creating the tables has completed.")

def populateVideoTable(videoName):
    try:
       Video.create(video_name=videoName, psm_side="left")
       Video.create(video_name=videoName, psm_side="right")
    except:
        pass

def populateKinematic2DTable(kinematicData, videoName, psmSide, frame, Null=False): 
    id = Video.get(Video.video_name == videoName).id
    if not Null:  
        if psmSide == "left":            
            Kinematics2D.create(
                video_name = id,
                frame = frame,
                psm_origo_x = kinematicData["ORIGO_LEFT_PSM"][0],
                psm_origo_y = kinematicData["ORIGO_LEFT_PSM"][1],
                psm_leftFromOrigo_x = kinematicData["LEFT_FROM_ORIGO_LEFT_PSM"][0],
                psm_leftFromOrigo_y = kinematicData["LEFT_FROM_ORIGO_LEFT_PSM"][1],
                psm_rightFromOrigoUp_x = kinematicData["UPRIGHT_FROM_ORIGO_LEFT_PSM"][0],
                psm_rightFromOrigoUp_y = kinematicData["UPRIGHT_FROM_ORIGO_LEFT_PSM"][1],
                psm_rightFromOrigoDown_x = kinematicData["DOWNRIGHT_FROM_ORIGO_LEFT_PSM"][0],
                psm_rightFromOrigoDown_y = kinematicData["DOWNRIGHT_FROM_ORIGO_LEFT_PSM"][1],
                psm_belowOrigo_x = kinematicData["BELOW_ORIGO_LEFT_PSM"][0],
                psm_belowOrigo_y = kinematicData["BELOW_ORIGO_LEFT_PSM"][1],
                psm_aboveOrigo_x = kinematicData["ABOVE_ORIGO_LEFT_PSM"][0],
                psm_aboveOrigo_y = kinematicData["ABOVE_ORIGO_LEFT_PSM"][1],
            )
        elif psmSide == "right":
            Kinematics2D.create(
                video_name = id + 1,
                frame = frame,
                psm_origo_x = kinematicData["ORIGO_RIGHT_PSM"][0],
                psm_origo_y = kinematicData["ORIGO_RIGHT_PSM"][1],
                psm_leftFromOrigo_x = kinematicData["LEFT_FROM_ORIGO_RIGHT_PSM"][0],
                psm_leftFromOrigo_y = kinematicData["LEFT_FROM_ORIGO_RIGHT_PSM"][1],
                psm_rightFromOrigoUp_x = kinematicData["UPRIGHT_FROM_ORIGO_RIGHT_PSM"][0],
                psm_rightFromOrigoUp_y = kinematicData["UPRIGHT_FROM_ORIGO_RIGHT_PSM"][1],
                psm_rightFromOrigoDown_x = kinematicData["DOWNRIGHT_FROM_ORIGO_RIGHT_PSM"][0],
                psm_rightFromOrigoDown_y = kinematicData["DOWNRIGHT_FROM_ORIGO_RIGHT_PSM"][1],
                psm_belowOrigo_x = kinematicData["BELOW_ORIGO_RIGHT_PSM"][0],
                psm_belowOrigo_y = kinematicData["BELOW_ORIGO_RIGHT_PSM"][1],
                psm_aboveOrigo_x = kinematicData["ABOVE_ORIGO_RIGHT_PSM"][0],
                psm_aboveOrigo_y = kinematicData["ABOVE_ORIGO_RIGHT_PSM"][1],
            )
    else:
        if psmSide == "left":
            Kinematics2D.create(
                video_name = id,
                frame = frame,
                psm_origo_x = kinematicData["ORIGO_LEFT_PSM"],
                psm_origo_y = kinematicData["ORIGO_LEFT_PSM"],
                psm_leftFromOrigo_x = kinematicData["LEFT_FROM_ORIGO_LEFT_PSM"],
                psm_leftFromOrigo_y = kinematicData["LEFT_FROM_ORIGO_LEFT_PSM"],
                psm_rightFromOrigoUp_x = kinematicData["UPRIGHT_FROM_ORIGO_LEFT_PSM"],
                psm_rightFromOrigoUp_y = kinematicData["UPRIGHT_FROM_ORIGO_LEFT_PSM"],
                psm_rightFromOrigoDown_x = kinematicData["DOWNRIGHT_FROM_ORIGO_LEFT_PSM"],
                psm_rightFromOrigoDown_y = kinematicData["DOWNRIGHT_FROM_ORIGO_LEFT_PSM"],
                psm_belowOrigo_x = kinematicData["BELOW_ORIGO_LEFT_PSM"],
                psm_belowOrigo_y = kinematicData["BELOW_ORIGO_LEFT_PSM"],
                psm_aboveOrigo_x = kinematicData["ABOVE_ORIGO_LEFT_PSM"],
                psm_aboveOrigo_y = kinematicData["ABOVE_ORIGO_LEFT_PSM"],
            )

        elif psmSide == "right":
            Kinematics2D.create(
                video_name = id + 1,
                frame = frame,
                psm_origo_x = kinematicData["ORIGO_RIGHT_PSM"],
                psm_origo_y = kinematicData["ORIGO_RIGHT_PSM"],
                psm_leftFromOrigo_x = kinematicData["LEFT_FROM_ORIGO_RIGHT_PSM"],
                psm_leftFromOrigo_y = kinematicData["LEFT_FROM_ORIGO_RIGHT_PSM"],
                psm_rightFromOrigoUp_x = kinematicData["UPRIGHT_FROM_ORIGO_RIGHT_PSM"],
                psm_rightFromOrigoUp_y = kinematicData["UPRIGHT_FROM_ORIGO_RIGHT_PSM"],
                psm_rightFromOrigoDown_x = kinematicData["DOWNRIGHT_FROM_ORIGO_RIGHT_PSM"],
                psm_rightFromOrigoDown_y = kinematicData["DOWNRIGHT_FROM_ORIGO_RIGHT_PSM"],
                psm_belowOrigo_x = kinematicData["BELOW_ORIGO_RIGHT_PSM"],
                psm_belowOrigo_y = kinematicData["BELOW_ORIGO_RIGHT_PSM"],
                psm_aboveOrigo_x = kinematicData["ABOVE_ORIGO_RIGHT_PSM"],
                psm_aboveOrigo_y = kinematicData["ABOVE_ORIGO_RIGHT_PSM"],
            )
        

def getVideoId(videoName):
    try:
        left = (Video.get(Video.video_name==videoName, Video.psm_side == "left")).id
    except:
        left = None
    try:
        right = (Video.get(Video.video_name==videoName, Video.psm_side == "right")).id
    except:
        right = None
    return left, right

def deleteExistingKinematicRows(videoName, psm_side):
    leftId, rightId = getVideoId(videoName)
    if psm_side == 'right' and rightId is not None:
        return Kinematics2D.delete().where(Kinematics2D.video_name == rightId)
    elif psm_side == 'left' and leftId is not None:
        return Kinematics2D.delete().where(Kinematics2D.video_name == leftId)
    else:
        return None

def deleteExistingVideoRows(videoName):
    return Video.delete().where(Video.video_name == videoName)