import filesManagement as fiMan

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
    route = 'files/nosigned'
    i = 1
    print("Select a document to sing")
    files = fiMan.listFiles(route)
    for file in files:
        print("" + str(i) +". "+file)
        i = i + 1
    
    pos = int(input("\nYour option: "))
    file_sel_name = files[pos-1]
    print(file_sel_name)
    #Se desencripta los archivos que estan
    #Se muestra el archivo al directivo
    fiMan.openFile(route+ '/' + file_sel_name,"","")
    
    return 0




def chooseADocument():
   return 0

def docToSign():
    return 0

def signedDocuments():
    return 0

        
directivePrincipalMenu()   