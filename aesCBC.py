from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
#from filesManagement import savefile, readFile

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



