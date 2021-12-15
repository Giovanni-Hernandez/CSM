import filesManagement as fiMan
import aesCBC as Aes
import rsa2048 as Rsa
from datetime import datetime
import time


def directivePrincipalMenu(username):
    directive = username
    print("Welcome directive " + directive)
    option = 0

    while (option != 4):
        print('D I R E C T I V E   M E N U\n')
        print('\t1. Sign a document')
        print('\t2. Documents to sign')
        print('\t3. Signed documents')
        print('\t4. Log out')
        print('\nSelect an option: ', end='')

        option = int(input())

        if(option == 1):
            #Aqui se va a la parte de firmar un documento
            signDocument(directive)

        if(option == 2):
            #Aqui muestra los archivos que faltan por firmar
            docToSign(directive)

        if(option == 3):
            #Aqui simplemente muestra un reporte
            signedDocuments(directive)

def signDocument(directive):
    
    #Routes of the directive
     
    routeDirective = 'directives/' + directive + "/"
    routeDocsDirective = 'directives/' + directive + '/documents/'
    routePrivDirective = 'directives/' + directive + '/private/'
    routeCEO = 'ceo/documents/'
    
    #Se extraen las llaves AES y RSA de un usuario
    key = fiMan.readFile64(routePrivDirective, "key", ".aes")
    keyRSACEOPub = Rsa.readRSAPublicKey(routeDirective, "CEOpub")
    keyRSAPrivate = Rsa.readRSAPrivateKey(routePrivDirective, "priv")

    #Le mostamos al usuario los documentos que estan disponibles para firmar
    i = 1
    print('S I G N  A  D O C U M E N T\n')
    print("Select a document to sign")
    
    files = verifiDocume(directive)

    if not files:
        return print("You already signed all the documents :)")

    #files = fiMan.listFiles(routeDocsDirective)
    for file in files:
        print("\t" + str(i) +". "+file)
        i = i + 1
    
    pos = int(input("\nYour option: "))
    file_sel_name = files[pos-1]

    #Se desencripta los archivos que estan en la carpeta que seleccione
    routeDocSel = routeDocsDirective + file_sel_name + "/"
    document_sel = fiMan.readFile64(routeDocSel, "encFile", ".enc")
    document_sel_iv = fiMan.readFile64(routeDocSel, "iv", ".data")

    print("\nDecrypting " + file_sel_name +"...")
    document_desc = Aes.decryptAES(key, document_sel, document_sel_iv)
    fiMan.saveFile(routeDocSel, file_sel_name, '', document_desc)
    time.sleep(3)
    print("Opening " + file_sel_name +"...")
    #Se muestra el archivo al directivo
    fiMan.openFile2(routeDocSel, file_sel_name ,"")

    res = int(input("\nDo you want to sign '" + file_sel_name + "'?\n\t1.Yes\n\t2.No\nYour Option: "))
    if(res == 1):
        #Se firma el documento con RSA
        print("Signing "+ file_sel_name +"...")
        signature = Rsa.signSHA256(document_sel, keyRSAPrivate)
        time.sleep(2)
        #Se guardan los arhcivos con la extension en la carpeta del director
        print("Sending "+ file_sel_name +" to the CEO...")
        fiMan.savefile64(routeDocSel, "encFile",".enc.sig", signature )
        time.sleep(2)

        #Se guarda los archivos en la direccion del CEO
        routeCEO = routeCEO + file_sel_name + '/signatures/' + directive + "/"
        fiMan.savefile64(routeCEO, "encFile",".enc.sig", signature )
        
        print("\n'"+file_sel_name+"' successfully signed and sent to CEO :) \n")
    
    #Borrando el archivo para evitar mostrarlo
    band = True
    while(band != False):
        try:
            fiMan.deleteFile(routeDocSel + "/" + file_sel_name)
            band = False
        except:
            input("Please close the file " + file_sel_name + ".pdf, then press enter ")

def docToSign(directive):
    routeDocsDirective = 'directives/' + directive + '/documents/'
    routeReport = 'directives/' + directive + '/Report.txt'
    files = fiMan.listFiles(routeDocsDirective)
    missing = []

    #La fecha del reporte
    date = fiMan.dateNow()

    #Realizamos el recorrido 

    for file in files:
        route = routeDocsDirective + '/' + file + "/"
        band = fiMan.existsDir(route, "encFile.enc.sig")
        if(band == False):
            missing.append(file)

    #Creando el txt para mostrar el reporte
    
    file = open(routeReport, 'w')
    file.write("CEO Security Master\n\nReport of Documents to Sign\n\n")
    file.write("Directive: " + directive)

    #Vemos si hay o no documentos en la carpeta
    if not missing:
        file.write("\n\nYou already signed all the documents\n")
    else:
        file.write("\n\nThe documents to sign are:\n")
        for files in missing:
            file.write("\t*" + files + "\n")
    
    file.write(date)
    file.close()

    fiMan.openFile2(routeReport, "", "")


def signedDocuments(directive):
    routeDocsDirective = 'directives/' + directive + '/documents/'
    files = fiMan.listFiles(routeDocsDirective)
    already = []
    routeReport = 'directives/' + directive + '/Report.txt'
    
    #Obtenemos la fecha de hoy
    date = fiMan.dateNow()

    #Realizamos el recorrido 

    for file in files:
        route = routeDocsDirective + '/' + file + "/"
        band = fiMan.existsDir(route, "encFile.enc.sig")
        if(band == True):
            already.append(file)

    #Creando el txt para mostrar el reporte
    
    file = open(routeReport, 'w')
    file.write("CEO Security Master\n\nReport of Signed Documents\n\n")
    file.write("Directive: " + directive)

    #Vemos si hay o no documentos en la carpeta
    if not already:
        file.write("\n\nYou have not signed any document yet\n")
    else:
        file.write("\n\nThe documents that you have signed are:\n")
        for files in already:
            file.write("\t*" + files + "\n")
    
    file.write(date)
    file.close()

    fiMan.openFile2(routeReport, "", "")
   
def verifiDocume(directive):
    routeDocsDirective = 'directives/' + directive + '/documents/'
    files = fiMan.listFiles(routeDocsDirective)
    missing = []

    for file in files:
        route = routeDocsDirective + '/' + file + "/"
        band = fiMan.existsDir(route, "encFile.enc.sig")
        if(band == False):
            missing.append(file)

    return missing



#directivePrincipalMenu("sandy")   