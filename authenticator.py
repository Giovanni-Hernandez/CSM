#Generar un factor de autentificación en 2 pasos
import pyotp
import qrcode
from os import system

def generate(username):
    secret = pyotp.random_base32() 
    with open('secret.txt', mode='w') as f: f.write(secret)
    print("Secret Key:", secret)
    file = open("../CSM/users/"+username, "a")
    file.write(secret)
    file.close()

    totp_object = pyotp.TOTP(secret)
    #print(totp_object.now()) #Print the OTP
    qr_text = totp_object.provisioning_uri(name=username, issuer_name="CEO Security Master")
    #print(qr_text)

    #Convertir el código en QR
    img = qrcode.make(qr_text)
    img.show()

def verificate_otp(username):
    file1 = open("../CSM/users/"+username, "r")
    verify = file1.read().splitlines()
    file1.close()
    totp_object = pyotp.TOTP(verify[2])
    system('cls')
    print("¡Good correct username and password! Now 2 factor verification")
    get_otp = input("Input the OTP\n[>]: ")

    return (totp_object.verify(otp = get_otp))
