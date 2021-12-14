import filesManagement as fiMan
import aesCBC as Aes
import rsa2048 as Rsa


def directivePrincipalMenu(username):
    directive = username
    print("Welcome directive " + directive)
    option = 0

    while (option != 4):
        print('D I R E C T I V E   M E N U\n')
        print('1. Sign a document')
        print('2. Documents to sign')
        print('3. Signed documents')
        print('4. Exit app')
        print('\nSelect an option: ', end='')

        option = int(input())

        if(option == 1):
            #Aqui se va a la parte de firmar un documento
            singDocument(directive)

        if(option == 2):
            #Aqui muestra los archivos que faltan por firmar
            chooseADocument()

        if(option == 3):
            #Aqui simplemente muestra un reporte
            docToSign()

def singDocument(directive):
    
    #Routes of the directive
     
    routeDirective = 'directives/' + directive + "/"
    routeDocsDirective = 'directives/' + directive + '/documents/'
    routePrivDirective = 'directives/' + directive + '/private/'
    routeCEO = 'ceo/documents/'
    
    #route = 'directives/Carlos/private/'
    #routeCEO = 'ceo/'

    #Se extraen las llaves AES y RSA de un usuario
    key = fiMan.readFile64(routePrivDirective, "key", ".aes")
    keyRSACEOPub = Rsa.readRSAPublicKey(routeDirective, "CEOpub")
    keyRSAPrivate = Rsa.readRSAPrivateKey(routePrivDirective, "priv")

    #Le mostamos al usuario los documentos que estan disponibles para firmar
    i = 1
    print("Select a document to sing")
    
    files = fiMan.listFiles(routeDocsDirective)
    for file in files:
        print("" + str(i) +". "+file)
        i = i + 1
    
    pos = int(input("\nYour option: "))
    file_sel_name = files[pos-1]

    #Se desencripta los archivos que estan en la carpeta que seleccione
    routeDocSel = routeDocsDirective + file_sel_name + "/"
    document_sel = fiMan.readFile64(routeDocSel, "encFile", ".enc")
    document_sel_iv = fiMan.readFile64(routeDocSel, "iv", ".data")

    document_desc = Aes.decryptAES(key, document_sel, document_sel_iv)
    fiMan.saveFile(routeDocSel, file_sel_name, '', document_desc)

    #Se muestra el archivo al directivo
    fiMan.openFile(routeDocSel, file_sel_name ,"")

    res = int(input("Do you want to sign '" + file_sel_name + "'?\n1.Yes\n2.No\nYour Option: "))
    if(res == 1):
        #Se firma el documento con RSA
        signature = Rsa.signSHA256(document_sel, keyRSAPrivate)
    
        #Se guardan los arhcivos con la extension en la carpeta del director
        fiMan.savefile64(routeDocSel, "encFile",".enc.sig", signature )

        #Se guarda los archivos en la direccion del CEO
        routeCEO = routeCEO + file_sel_name + '/signatures/' + directive + "/"
        fiMan.savefile64(routeCEO, "encFile",".enc.sig", signature )
        
        print("'"+file_sel_name+"' successfully signed and sent to CEO :) \n")
    
    #Borrando el archivo para evitar mostrarlo
    band = True
    while(band != False):
        try:
            fiMan.deleteFile(routeDocSel + "/" + file_sel_name)
            band = False
        except:
            input("Please close the file " + file_sel_name + ".pdf, then press enter ")

def chooseADocument():
   return 0

def docToSign():
    return 0

def signedDocuments():
    return 0

directivePrincipalMenu("")   