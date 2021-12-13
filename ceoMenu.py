from os import system
import sys
import filesManagement as fm
import rsa2048 as rsa
import aesCBC as aes

ceoRoute = 'ceo/'
privateFolder = 'private/'
ceoDirectivesRoute = 'ceo/directives/'
mode = 0o666


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
            chooseADocument()

        if(option == 2):
            input()

        if(option == 3):
            input()


def chooseADocument():

    folder = ceoRoute + privateFolder + 'documents/'

    # Available documents are shown
    listOfFiles = fm.listFiles(folder)

    system('cls')

    i = 1

    print("A V A I L A B L E   D O C U M E N T S\n")

    for file in listOfFiles:
        print("" + str(i) + ". " + file)
        i = i + 1

    fileSelected = int(input("\nChoose a file: "))
    filename = listOfFiles[fileSelected - 1]

    # Bytes from file are read
    contentFile = fm.readFile(folder, filename, '')

    # File is ciphered for all directives
    listOfDirectives = fm.listDir(ceoDirectivesRoute)

    # Getting CEO's private key
    CEOPrivKey = rsa.readRSAPrivateKey(ceoRoute + 'private/', 'CEOpriv')

    # Encryption is done as many times as there are directives
    for directive in listOfDirectives:
        # Reading the director's encrypted AES key file
        dirEncAESKey = fm.readFile(
            ceoDirectivesRoute + directive + '/', 'encryptedKey', '.aes')

        # Decrypting director's AES Key
        decAESKey = rsa.decryptRSA(dirEncAESKey, CEOPrivKey)

        # Encrypting file using directive's AES key
        encContent, iv = aes.encryptAES(decAESKey, contentFile)

        # Document directory is created
        fm.createDir('directives/' + directive + '/documents/', filename)
        fileDir = 'directives/' + directive + '/documents/' + filename + '/'

        # Sending ecrypted document and IV to directive
        fm.saveFile(fileDir, 'encryptedFile', '.enc', contentFile)
        fm.saveFile(fileDir, 'iv', '.csv', contentFile)

    print("Documents have been sent to each directive")


#ceoPrincipalMenu()
