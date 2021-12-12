from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from filesManagement import savefile64, readFile64, saveFile, readFile

#Generates random 256-bit AES key
def generate256Key():
    return get_random_bytes(32)

#Performs AES encryption and returns encrypted bytes and random IV
#used for encryption
def encryptAES(key, msgBytes):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.encrypt(pad(msgBytes, 16)), cipher.iv

#Performs AES decryption
def decryptAES(key, cipherBytes, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(cipherBytes), 16)

#key = generate256Key()
#msg = b'Codigo para ver que si funciona'
#cipherBytes, iv = encryptAES(key, msg)
#decipherBytes = decryptAES(key, cipherBytes, iv)
#print(str(decipherBytes))

#key = generate256Key()
#savefile64("directives/Carlos/", "CarlosAES", ".aes", key)

#Para cifrar el documento
#key = readFile64("directives/Carlos/", "CarlosAES", ".aes")
#libro = readFile("files/nosigned/", "Redes", ".pdf")
#cifra_libro, iv = encryptAES(key, libro)
#savefile64("directives/Carlos/Redes/", "Redes", ".enc",cifra_libro)
#savefile64("directives/Carlos/Redes/", "RedesIV", ".enc",iv)
#libro = readFile64("directives/Carlos/Redes/", "Redes", ".enc")
#iv = readFile64("directives/Carlos/Redes/", "RedesIV", ".enc")
#des = decryptAES(key, libro, iv)
#saveFile("directives/Carlos/Redes/", "Redes", ".pdf", des)