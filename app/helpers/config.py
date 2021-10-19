import json
import helpers.globals

def getConfig(configFile):
    """
    Summary:
    Parse the configuration file and return it's values.

    Parameters:
    configFile (str): Path to the configuration json file.

    Returns: 
    dict: The configuration values as a dictionary object.
    """
    with open(configFile) as conf:
        confData = json.load(conf)
        if not helpers.globals.CONFFILEACCESSED:
            helpers.globals.CONFFILEPATH = configFile
            helpers.globals.CONFFILEACCESSED = True
    return confData