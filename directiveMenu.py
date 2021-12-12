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
    route = 'directives/Carlos/'
    key = fiMan.readFile64(route, "CarlosAES", ".aes")
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



    #Se cifra el documento con su AES
    #file = fiMan.readFile(route + '/' + file_sel_name, "", "")
    
    #cifra, iv = Aes.encryptAES(key, file)
    
    #Se firma el documento con RSA
    #signature = Rsa.signSHA256(cifra, keyCEO)
    
    #fiMan.saveFile64(route, )

    return 0





def chooseADocument():
   return 0

def docToSign():
    return 0

def signedDocuments():
    return 0

directivePrincipalMenu()   