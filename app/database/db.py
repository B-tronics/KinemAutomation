from peewee import SqliteDatabase
from helpers.globals import DBNAME
from helpers.log import createLogger

# Create the database instance
db = SqliteDatabase(DBNAME, pragmas={'foreign_keys': 1})


