import base64
from os import system
import sys
from rsa.pkcs1 import verify
import filesManagement as fm
import rsa2048 as rsa
import aesCBC as aes
import time

ceoRoute = 'ceo/'
privateFolder = 'private/'
ceoDirectivesRoute = 'ceo/directives/'
ceoDocuments = 'ceo/documents/'
ceoReports = ceoRoute + privateFolder + 'reports/'


def ceoPrincipalMenu():

    option = 0

    while (option != 4):
        system('cls')
        print('C E O   M E N U\n')
        print('\t1. Choose a document')
        print('\t2. Verify signatures')
        print('\t3. Delete a document')
        print('\t4. Exit app')
        print('\nSelect an option: ', end='')

        option = int(input())

        if(option == 1):
            encryptDocument()

        if(option == 2):
            verification()

        if(option == 3):
            deleteDocument()


# Function to perform file encryption
def encryptDocument():

    folder = ceoRoute + privateFolder + 'documents/'
    filename = chooseADocument(folder)

    ceoFileRoute = ceoDocuments + filename + '/'

    if(fm.existsDir(ceoFileRoute, '')):
        system('cls')
        print('W A R N I N G\n')
        print('\tThe file ' + filename + ' has already been encrypted\n')
        pause()
        return False

    print("------------- Encryption -------------\n")
    # Bytes from file are read
    contentFile = fm.readFile(folder, filename, '')

    # Getting CEO's private key
    CEOPrivKey = rsa.readRSAPrivateKey(ceoRoute + 'private/', 'CEOpriv')
    print("Getting CEO's RSA private key...")
    # time.sleep(2)

    # File is ciphered for all directives
    listOfDirectives = fm.listDir(ceoDirectivesRoute)

    # Create a directory for the CEO to save everything about this document
    fm.createDir(ceoDocuments, filename)
    fm.createDir(ceoDocuments + filename + '/', 'signatures')

    ceoFileRouteSig = ceoFileRoute + 'signatures/'

    # Encryption is done as many times as there are directives
    for directive in listOfDirectives:
        # Reading the director's encrypted AES key file
        dirEncAESKey = fm.readFile64(
            ceoDirectivesRoute + directive + '/private/', 'encryptedKey', '.aes')

        print("------------- " + directive + " -------------\n")

        # Decrypting director's AES Key
        decAESKey = base64.b64decode(rsa.decryptRSA(dirEncAESKey, CEOPrivKey))
        print("Decrypting AES key with CEO's private RSA key...")
        # time.sleep(2)

        # Encrypting file using directive's AES key
        encContent, iv = aes.encryptAES(decAESKey, contentFile)
        print("Encrypting file with AES key...")
        # time.sleep(2)

        # Document directory is created
        fm.createDir('directives/' + directive + '/', 'documents')
        fm.createDir('directives/' + directive + '/documents/', filename)
        fileDir = 'directives/' + directive + '/documents/' + filename + '/'

        # Sending ecrypted document and IV to directive
        fm.savefile64(fileDir, 'encFile', '.enc', encContent)
        fm.savefile64(fileDir, 'iv', '.data', iv)
        print("Encryption stored in: " + 'directives/' +
              directive + '/documents/' + filename + '/encFile.enc')
        print("IV stored in: " + 'directives/' +
              directive + '/documents/' + filename + '/iv.data\n')
        # time.sleep(2)

        # Create directory to know this director has to sign this document
        fm.createDir(ceoFileRouteSig, directive)
        fm.savefile64(ceoFileRouteSig + '/' + directive +
                      '/', 'encFile', '.enc', encContent)

    pause()


def verification():
    option = 0

    system('cls')
    print('S I G N A T U R E S   V E R I F I C A T I O N\n')
    print('\t1. Verify a document')
    print('\t2. Verify all documents')
    print('\t3. Cancel')
    print('\nSelect an option: ', end='')

    option = int(input())

    if(option == 1):
        singleDocument()

    if(option == 2):
        allDocuments()


def singleDocument():
    # Getting al documents available for signature
    filename = chooseADocument(ceoDocuments)

    date = fm.dateNow()
    fullDate = fm.fullDate()
    reportName = ceoReports + 'singleDocumentSignatures' + fullDate + '.txt'

    f = open(reportName, 'w')
    f.write('CEO Security Master\n\n')
    f.write('Report of signatures of a single document\n\n')
    f.write('File: ' + filename + '\n\n')
    f.write("\tDirectives' signatures: \n\n")

    verifySignatures(filename, f)

    f.write(date)
    f.close()

    print("\nReporte file stored in: " + reportName + "\n")
    # time.sleep(2)

    pause()


def allDocuments():

    date = fm.dateNow()
    fullDate = fm.fullDate()
    reportName = ceoReports + 'allDocumentsSignatures' + fullDate + '.txt'

    f = open(reportName, 'w')
    f.write('CEO Security Master\n\n')
    f.write('Report of signatures of all documents')

    listOfDocuments = fm.listDir(ceoDocuments)

    for document in listOfDocuments:
        f.write('\n\nFile: ' + document + '\n\n')
        f.write("\tDirectives' signatures: \n\n")

        verifySignatures(document, f)

    f.write(date)
    f.close()

    print("\nReporte file stored in: " + reportName + "\n")
    # time.sleep(2)

    pause()


# Function to verify signatures of a document
def verifySignatures(filename, f):

    print("------------- " + filename + " -------------\n")
    # time.sleep(2)

    # Getting all directives that can sign this document
    signaturesRoute = ceoDocuments + filename + '/signatures/'
    listOfDir = fm.listDir(signaturesRoute)

    for directive in listOfDir:

        print("------------- " + directive + " -------------\n")
        # time.sleep(2)

        # Getting directives public key
        routeDirective = ceoDirectivesRoute + '/' + directive + '/'
        keyRSADirPub = rsa.readRSAPublicKey(routeDirective, "pub")
        print(directive + "'s RSA public key retrieved")
        # time.sleep(2)

        # Getting encrypted file and signature
        routeDirSignature = signaturesRoute + directive + '/'
        document = fm.readFile64(routeDirSignature, "encFile", ".enc")
        signature = fm.readFile64(routeDirSignature, "encFile", ".enc.sig")
        print("Retrieving encrypted file and signature...")
        # time.sleep(2)

        print("Verifying signature with RSA public key...")
        # time.sleep(2)

        # Checking if signature has been done
        if(signature == False):
            f.write('\t\t* ' + directive + ' has not signed this document\n')
            print(directive + ' has not signed this document\n')
            # time.sleep(2)
        # Verify signature
        elif(rsa.verifySHA256(document, signature, keyRSADirPub)):
            f.write('\t\t* ' + directive + "'s signature is valid\n")
            print(directive + "'s signature is valid\n")
            # time.sleep(2)
        else:
            f.write('\t\t* ' + directive + "'s signature IS NOT VALID!!!\n")
            print(directive + "'s signature IS NOT VALID!!!\n")
            # time.sleep(2)


# Function to delete document
def deleteDocument():
    filename = chooseADocument(ceoDocuments)

    # Getting users' routes
    sigDocumentRoute = ceoDocuments + filename + '/signatures/'
    dirRoute = 'directives/'

    # Getting each directives document route if it exists
    listOfDir = fm.listDir(sigDocumentRoute)

    # Deleting document for each directive
    for directive in listOfDir:
        dirDocumentRoute = dirRoute + directive + '/documents/' + filename
        fm.deleteDir(dirDocumentRoute)

    # Deleting document for CEO
    fm.deleteDir(ceoDocuments + filename)

    print("\nThe document " + filename +
          " and related files have been deleted\n")
    pause()


# Function to choose a document
def chooseADocument(route):

    # Available documents are shown
    listOfFiles = fm.listFiles(route)

    i = 1

    system('cls')
    print("A V A I L A B L E   D O C U M E N T S\n")

    for file in listOfFiles:
        print("\t" + str(i) + ". " + file)
        i = i + 1

    fileSelected = int(input("\nChoose a file: "))
    filename = listOfFiles[fileSelected - 1]

    return filename


# Function to pause execution
def pause():
    input('Enter any key to continue...')


ceoPrincipalMenu()
