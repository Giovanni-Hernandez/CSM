import base64
from os import system
import sys

from rsa.pkcs1 import verify
import filesManagement as fm
import rsa2048 as rsa
import aesCBC as aes

ceoRoute = 'ceo/'
privateFolder = 'private/'
ceoDirectivesRoute = 'ceo/directives/'
ceoDocuments = 'ceo/documents/'


def ceoPrincipalMenu():

    option = 0

    while (option != 4):
        system('cls')
        print('C E O   M E N U\n')
        print('1. Choose a document')
        print('2. Verify signatures')
        print('3. Delete a document')
        print('4. Exit app')
        print('\nSelect an option: ', end='')

        option = int(input())

        if(option == 1):
            encryptDocument()

        if(option == 2):
            verification()

        if(option == 3):
            input()


def verification():
    option = 0

    while (option != 3):
        system('cls')
        print('S I G N A T U R E S   V E R I F I C A T I O N\n')
        print('1. Verify a document')
        print('2. Verify all documents')
        print('3. Cancel')
        print('\nSelect an option: ', end='')

        option = int(input())

        if(option == 1):
            singleDocument()

        if(option == 2):
            input()


def singleDocument():
    # Getting al documents available for signature
    filename = chooseADocument(ceoDocuments)
    verifySignature(filename)
    input()

    return 1


def verifySignature(filename):
    # Getting all directives that can sign this document
    signaturesRoute = ceoDocuments + filename + '/signatures/'
    listOfDir = fm.listDir(signaturesRoute)

    for directive in listOfDir:
        # Getting directives public key
        routeDirective = ceoDirectivesRoute + '/' + directive + '/'
        keyRSADirPub = rsa.readRSAPublicKey(routeDirective, "pub")

        # Getting encrypted file and signature
        routeDirSignature = signaturesRoute + directive + '/'
        document = fm.readFile64(routeDirSignature, "encFile", ".enc")
        signature = fm.readFile64(routeDirSignature, "encFile", ".enc.sig")

        # Checking if signature has been done
        if(signature == False):
            print(directive + ' has not signed this document')
        # Verify signature
        elif(rsa.verifySHA256(document, signature, keyRSADirPub)):
            print(directive + "'s signature is valid")
        else:
            print(directive + "'s signature IS NOT VALID!!!")


def chooseADocument(route):

    # Available documents are shown
    listOfFiles = fm.listFiles(route)

    i = 1

    system('cls')
    print("A V A I L A B L E   D O C U M E N T S\n")

    for file in listOfFiles:
        print("" + str(i) + ". " + file)
        i = i + 1

    fileSelected = int(input("\nChoose a file: "))
    filename = listOfFiles[fileSelected - 1]

    return filename


def encryptDocument():

    folder = ceoRoute + privateFolder + 'documents/'
    filename = chooseADocument(folder)

    # Bytes from file are read
    contentFile = fm.readFile(folder, filename, '')

    # Getting CEO's private key
    CEOPrivKey = rsa.readRSAPrivateKey(ceoRoute + 'private/', 'CEOpriv')

    # File is ciphered for all directives
    listOfDirectives = fm.listDir(ceoDirectivesRoute)

    # Create a directory for the CEO to save everything about this document
    fm.createDir(ceoDocuments, filename)
    fm.createDir(ceoDocuments + filename + '/', 'signatures')

    ceoFileRoute = ceoDocuments + filename
    ceoFileRouteSig = ceoFileRoute + '/signatures/'

    # Encryption is done as many times as there are directives
    for directive in listOfDirectives:
        # Reading the director's encrypted AES key file
        dirEncAESKey = fm.readFile64(
            ceoDirectivesRoute + directive + '/private/', 'encryptedKey', '.aes')

        # Decrypting director's AES Key
        decAESKey = base64.b64decode(rsa.decryptRSA(dirEncAESKey, CEOPrivKey))

        # Encrypting file using directive's AES key
        encContent, iv = aes.encryptAES(decAESKey, contentFile)

        # Document directory is created
        fm.createDir('directives/' + directive + '/documents/', filename)
        fileDir = 'directives/' + directive + '/documents/' + filename + '/'

        # Sending ecrypted document and IV to directive
        fm.savefile64(fileDir, 'encFile', '.enc', encContent)
        fm.savefile64(fileDir, 'iv', '.data', iv)

        # Create directory to know this director has to sign this document
        fm.createDir(ceoFileRouteSig, directive)
        fm.savefile64(ceoFileRouteSig + '/' + directive +
                      '/', 'encFile', '.enc', encContent)

    print("Documents have been sent to each directive")
    input()


ceoPrincipalMenu()
