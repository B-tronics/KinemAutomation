import peewee
from .db import BaseDB

class Video(peewee.Model):
    id = peewee.PrimaryKeyField()
    video_name = peewee.TextField(unique=True)

class Kinematics(peewee.Model):
    """
    This class modells the data which is gained from the video files processed.
    """
    id = peewee.PrimaryKeyField()
    video_name = peewee.ForeignKeyField(Video)
    camera_number = peewee.IntegerField
    frame = peewee.IntegerField
    psm_left_pos_x = peewee.FloatField()
    psm_left_pos_y = peewee.FloatField()
    psm_left_pos_z = peewee.FloatField()
    psm_right_pos_x = peewee.FloatField()
    psm_right_pos_y = peewee.FloatField()
    psm_right_pos_z = peewee.FloatField()

class TestDbKinematics(peewee.Model):
    id = peewee.PrimaryKeyField()
    P1_x_coordinate = peewee.IntegerField()
    P1_y_coordinate = peewee.IntegerField()
    P2_x_coordinate = peewee.IntegerField()
    P2_y_coordinate = peewee.IntegerField()
    P3_x_coordinate = peewee.IntegerField()
    P3_y_coordinate = peewee.IntegerField()
    P4_x_coordinate = peewee.IntegerField()
    P4_y_coordinate = peewee.IntegerField()
    P5_x_coordinate = peewee.IntegerField()
    P5_y_coordinate = peewee.IntegerField()
    P6_x_coordinate = peewee.IntegerField()
    P6_y_coordinate = peewee.IntegerField()

    class Meta:
        database = BaseDB.db