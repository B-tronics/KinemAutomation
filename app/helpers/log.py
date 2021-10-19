import logging

def createLogger(name, logfile_name):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Create handler
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(logfile_name, mode='a')    

    # Create formatter and add it to handler
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(format)

    # Add handler to the logger
    logger.addHandler(handler)
    return logger
