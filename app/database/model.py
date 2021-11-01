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
    video_name = TextField(unique=True)

class Kinematics(BaseModel):
    video_name = ForeignKeyField(Video)
    frame = IntegerField()
    psm_left_pos_x = FloatField()
    psm_left_pos_y = FloatField()
    psm_left_pos_z = FloatField()
    psm_right_pos_x = FloatField()
    psm_right_pos_y = FloatField()
    psm_right_pos_z = FloatField()

def createTables():
    try:
        db.connect()
    except:
        logger.warning("Connecting to the database has failed.")
        exit()
    try:
        db.create_tables([Video, Kinematics])
    except:
        logger.warning("Creating the tables has failed.")

    logger.info("Creating the tables has completed.")

def populateVideoTable(videoName):
    try:
       Video.create(video_name=videoName)
    except:
        pass

def populateKinematicTable(kinematicData):
    pass