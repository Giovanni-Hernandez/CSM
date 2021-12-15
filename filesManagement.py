import base64
import subprocess
import os
from datetime import datetime
import shutil

# Saves a file in a route with specific extension using base 64


def savefile64(route, filename, extension, contentBytes):
    f = open(route + filename + extension, 'wb')
    f.write(base64.b64encode(contentBytes))
    f.close()

# Reads bytes from file in base 64


def readFile64(route, filename, extension):
    try:
        f = open(route + filename + extension, 'rb')
    except IOError:
        return False

    content = base64.b64decode(f.read())
    f.close()

    return content

# Reads bytes from file


def readFile(route, filename, extension):

    try:
        f = open(route + filename + extension, 'rb')
    except IOError:
        return False

    content = f.read()
    f.close()
    return content

# Saves a file in a route with specific extension


def saveFile(route, filename, extension, contentBytes):
    f = open(route + filename + extension, 'wb')
    f.write(contentBytes)
    f.close


# Open a file in any format
def openFile(route, filename, extension):
    direccion = os.path.abspath(os.getcwd()) + "/" + \
        route + filename + extension
    subprocess.Popen(direccion, shell=True)

# Return a list of all documents that are in a carpet


def listFiles(route):
    return os.listdir(route)

# Delete a file that you select


def deleteFile(route):
    os.remove(route)

# List of all directories inside a directory


def listDir(route):
    return [d for d in os.listdir(route) if os.path.isdir(os.path.join(route, d))]


# Create a directory
def createDir(route, name):
    if not os.path.exists(route + name):
        os.mkdir(route + name)


def existsDir(route, name):
    return os.path.exists(route + name)


def dateNow():
    now = datetime.now()
    return "\n\nThis report was generated on " + str(now.month) + "/" + str(now.day) + "/" + str(now.year) + " at " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)


def fullDate():
    now = datetime.now()
    return str(now.month) + "-" + str(now.day) + "-" + str(now.year) + "-" + str(now.hour) + str(now.minute) + str(now.second)


def deleteDir(route):
    try:
        shutil.rmtree(route)
    except OSError as e:
        print(f"Error:{ e.strerror}")
