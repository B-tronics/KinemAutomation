import sqlite3
from helpers.log import createLogger
from helpers.config import getConfig
from helpers.globals import CONFFILEPATH

logger = createLogger(__name__, getConfig(CONFFILEPATH)["LOGFILENAME"])

def readData(jigsawsPath, file_name):
    """
    Summary:
    Reads the Kinematic data table from the prepared jigsaws database and returns it's values

    Parameters:
    jigsawsPath (str): Path to the prepared jigsaws database.
    file_name (str): The name of the current videofile, which relates to the file_name columnn in the Video table.

    Returns:
    cursor: The data retrieved from the Kinematic table

    """
    try:
        connection = sqlite3.connect(jigsawsPath)
    except:
        logger.warning("Connecting to the JIGSAWS database failed.")
    else:    
        logger.info("Connecting to the JIGSAWS database succeded.")
        video_id = getVideoId(connection, file_name)
    try:
        jigsawsData = connection.execute(
                    f"SELECT frame, psm_right_pos_x, psm_right_pos_y, psm_right_pos_z, psm_left_pos_x, psm_left_pos_y, psm_left_pos_z FROM Kinematic WHERE video_id = '{video_id}'"
    )
    except:
        logger.warning("SQL command failed! Kinematic data could not be retrieved")
        exit()

    logger.info("Kinematic data from JIGSAWS has been retrieved succesfully.")
    connection.close()
    return jigsawsData

def getVideoId(connection ,file_name):
    video_id = connection.execute(
                f"SELECT id FROM Video WHERE file_name = '{file_name}'")
    for id in video_id:
        video_id = id[0]
    return video_id