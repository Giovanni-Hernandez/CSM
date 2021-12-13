import filesManagement as fiMan
import aesCBC as Aes
import rsa2048 as Rsa

def directivePrincipalMenu():

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
            singDocument()

        if(option == 2):
            #Aqui muestra los archivos que faltan por firmar
            chooseADocument()

        if(option == 3):
            #Aqui simplemente muestra un reporte
            docToSign()

def singDocument():
    #route 
    route = 'directives/Carlos/private/'
    routeCEO = 'ceo/'

    #Se extraen las llaves AES y RSA de un usuario
    key = fiMan.readFile64(route, "CarlosAES", ".aes")
    keyRSACEOPub = Rsa.readRSAPublicKey(routeCEO, "CEOpub")
    keyRSAPrivate = Rsa.readRSAPrivateKey(route, 'privada')

    #Cambiamos la ruta para que sea de los documentos
    route = 'directives/Carlos/documents/'

    #Le mostamos al usuario los documentos que estan disponibles para firmar
    i = 1
    print("Select a document to sing")
    files = fiMan.listFiles(route)
    for file in files:
        print("" + str(i) +". "+file)
        i = i + 1
    
    pos = int(input("\nYour option: "))
    file_sel_name = files[pos-1]

    #Se desencripta los archivos que estan en la carpeta que seleccione
    route = route + file_sel_name + "/"
    document_sel = fiMan.readFile64(route, file_sel_name, ".enc")
    document_sel_iv = fiMan.readFile64(route, file_sel_name+"IV", ".enc")

    document_desc = Aes.decryptAES(key, document_sel, document_sel_iv)
    fiMan.saveFile(route, file_sel_name, ".pdf", document_desc)

    #Se muestra el archivo al directivo
    fiMan.openFile(route, file_sel_name ,".pdf")

    res = int(input("Do you want to sign " + file_sel_name + ".pdf ?\n1.Yes\n2.No\nYour Option: "))
    if(res == 1):
        #Se firma el documento con RSA
        encryp_aes_key = Rsa.encryptRSA(key, keyRSACEOPub) #Se encripta la llave AES del directivo con la RSA publica del CEO
        sign = Rsa.signSHA256(encryp_aes_key, keyRSAPrivate) #Se firma con la lave RSA privada del director la llave encriptada de AES

        #Se guardan los arhcivos con la extension en la carpeta del director
        fiMan.savefile64(route, file_sel_name + "Carlos", ".enc.sig", sign)
        fiMan.savefile64(route, file_sel_name + "Carlos", ".aes", encryp_aes_key)

        #Se guarda los archivos en la direccion del CEO
        fiMan.savefile64(routeCEO+"/documents/"+file_sel_name+"/",file_sel_name + "Carlos", ".enc.sig",sign)
        fiMan.savefile64(routeCEO+"/documents/"+file_sel_name+"/",file_sel_name + "Carlos", ".aes",encryp_aes_key)
    
    #Borrando el archivo para evitar mostrarlo
    band = True
    while(band != False):
        try:
            fiMan.deleteFile(route+"/"+file_sel_name+".pdf")
            band = False
        except:
            input("Please close the file " + file_sel_name + ".pdf, then press enter ")

    print(file_sel_name+".pdf successfully signed and sent to CEO :) \n")


def chooseADocument():
   return 0

def docToSign():
    return 0

def signedDocuments():
    return 0

#directivePrincipalMenu()   