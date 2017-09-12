import os, sys


def createDirectory(path):
    if not directoryExists(path):
        os.makedirs(path)


def directoryExists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def fileExists(path):
    if os.path.isfile(path):
        return True
    else:
        return False


def createConfig(configString, file = "config.py"):
    with open(file, "w") as text_file:
        text_file.write(configString)

#def getConfig():
#    config_dir_path = os.path.expanduser("~/Source/python/configs/")
#    pybook_config_dir = config_dir_path + "pybook/"
#    sys.path.insert(0, os.path.expanduser(pybook_config_dir))
#    from config import config
#    return config
