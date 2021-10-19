import peewee
import os
import shutil
from helpers import log

logger = log.createLogger(__name__, "app.log")

class BaseDB:
    @classmethod
    def __init__(cls, databaseName, templateName):
        cls.db = cls.createDatabase(BaseDB, databaseName=databaseName, templateName=templateName)
        cls.tablesCreated = False

    def connect(cls, file):
        """
        Summary: Connect to the database defined
        
        Parameters:
        file (obj) : The database file to connect to

        Returns:
        obj: The database object
        """
        db = peewee.SqliteDatabase(file)
        db.connect()
        return db

    def createPath(cls, databaseName, templateName):
        """
        Create the folder structure which holds the database

        Parameters:
        db_name (str): Name of the newly created database (by default it should be diplomamunka.sqlite)
        template_name (str): Name of the template db (by default is should be template.sqlite)

        Returns:
        str: Path to the newly created database.
        """
        # check & create software data directory
        dir_config = os.path.expandvars('$APPDATA/diplomamunka').replace('$APPDATA', os.path.expanduser('~/.config'))

        try:
            os.makedirs(dir_config, exist_ok=True)
        except:
            logger.error("Creation of the database folder has failed.")
            exit()

        logger.info("Creation of the database folder has been successful.")
        file_db = os.path.join(dir_config, databaseName)

        # copy the template database to the working folder
        shutil.copyfile(templateName, file_db)

        return file_db
        
    def createDatabase(cls, databaseName, templateName):

        # Create the database and the folder structure
        file_db = cls.createPath(cls, databaseName, templateName)

        # Conect to the database
        db = cls.connect(cls, file_db)

        return db
    
    def createTables(cls, model):
        cls.db.create_tables([model])
        cls.tablesCreated = True
        





