from peewee import SqliteDatabase
from helpers.globals import DBNAME
from helpers.log import createLogger

# Create the database instance
db = SqliteDatabase(DBNAME, pragmas={'foreign_keys': 1})

import os

# Invoke the logger
logger = createLogger(__name__, "app.log")


def createDBPath(databaseName):
    # Create the database path
    dir = os.path.expandvars("$APPDATA/KinemAutomation").replace('$APPDATA', os.path.expanduser('~/.config'))

    # Try to create the folder structure
    try:
        os.makedirs(dir, exist_ok=True)
    except:
        logger.error("Creation of the database folder has failed.")
        exit()

    logger.info("Creation of the database folder has been successful.")

    # Create the fulle path to the database
    filePath = os.path.join(dir, databaseName)
    
    return filePath

