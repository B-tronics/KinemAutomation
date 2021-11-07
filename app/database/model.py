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

def populateKinematic2DTable(kinematicData, videoName, psmSide):
    
    Kinematics2D.create(
        video_name = Video.get(Video.video_name == videoName and Video.psm_side == psmSide).id,
        psm_origo_x = kinematicData["psm_origo_x"],
        psm_origo_y = kinematicData["psm_origo_y"],
        psm_leftFromOrigo_x = kinematicData["psm_leftFromOrigo_x"],
        psm_leftFromOrigo_y = kinematicData["psm_leftFromOrigo_y"],
        psm_rightFromOrigoUp_x = kinematicData["psm_rightFromOrigoUp_x"],
        psm_rightFromOrigoUp_y = kinematicData["psm_rightFromOrigoUp_y"],
        psm_rightFromOrigoDown_x = kinematicData["psm_rightFromOrigoDown_x"],
        psm_rightFromOrigoDown_y = kinematicData["psm_rightFromOrigoDown_y"],
        psm_belowOrigo_x = kinematicData["psm_belowOrigo_x"],
        psm_belowOrigo_y = kinematicData["psm_belowOrigo_y"],
        psm_aboveOrigo_x = kinematicData["psm_aboveOrigo_x"],
        psm_aboveOrigo_y = kinematicData["psm_aboveOrigo_y"],
    )

def getVideoId(videoName):
    left = (Video.get(Video.video_name==videoName, Video.psm_side == "left")).id
    right = (Video.get(Video.video_name==videoName, Video.psm_side == "right")).id
    return left, right

def deleteExistingKinematicRows(videoName, psm_side):
    leftId, rightId = getVideoId(videoName)
    if psm_side == 'right':
        return Kinematics2D.delete().where(Kinematics2D.video_name == rightId)
    elif psm_side == 'left':
        return Kinematics2D.delete().where(Kinematics2D.video_name == leftId)

def deleteExistingVideoRows(videoName):
    return Video.delete().where(Video.video_name == videoName)