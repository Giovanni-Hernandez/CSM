#Saves a file in a route with specific extension using base 64
def savefile(route, filename, extension, contentBytes):
    f = open(route + filename + extension, 'wb')
    f.write(base64.b64encode(contentBytes))
    f.close()

#Reads bytes from file in base 64
def readFile(route, filename, extension):
    f = open(route + filename + extension, 'rb')
    content = base64.b64decode(f.read())
    f.close()

    return content