import re

def getFileName(path):
    file_name = re.sub("\_capture..avi$", "", path)
    return file_name