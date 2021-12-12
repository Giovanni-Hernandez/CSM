import base64
import subprocess
import os

#Saves a file in a route with specific extension using base 64
def savefile64(route, filename, extension, contentBytes):
    f = open(route + filename + extension, 'wb')
    f.write(base64.b64encode(contentBytes))
    f.close()

#Reads bytes from file in base 64
def readFile64(route, filename, extension):
    f = open(route + filename + extension, 'rb')
    content = base64.b64decode(f.read())
    f.close()

    return content

#Reads bytes from file
def readFile(route, filename, extension):
    f = open(route + filename + extension, 'rb')
    content = f.read()
    f.close()
    return content

#Saves a file in a route with specific extension
def saveFile(route, filename, extension, contentBytes):
    f = open(route + filename + extension, 'wb')
    f.write(contentBytes)
    f.close


#Open a file in any format
def openFile(route, filename, extension):
    direccion = os.path.abspath(os.getcwd()) + "/" + route + filename + extension
    subprocess.Popen(direccion, shell = True)

#Return a list of all documents that are in a carpet
def listFiles(route):
    return os.listdir(route)

#savefile('', 'prueba', '.txt', b'Comida')
#print(str(readFile('', 'prueba', '.txt')))

