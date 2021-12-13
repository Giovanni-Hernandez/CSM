#Generar un factor de autentificación en 2 pasos
import pyotp
import qrcode
from os import system

# Generar un factor de verificación de 2 pasos mediante OTP
def generate(username):
    secret = pyotp.random_base32() 
    # Guardando llave secreta en la carpeta users en el archivo con el username
    print("Secret Key:", secret)
    file = open("../CSM/users/"+username, "a")
    file.write(secret)
    file.close()

    totp_object = pyotp.TOTP(secret)
    qr_text = totp_object.provisioning_uri(name=username, issuer_name="CEO Security Master")

    # Convertir el texto en QR
    img = qrcode.make(qr_text)
    img.show()
    img.save("../CSM/directives/"+username+"/private/qr.png")

# Verificacion del OTP  
def verificate_otp(username):
    file1 = open("../CSM/users/"+username, "r")
    verify = file1.read().splitlines()
    file1.close()
    totp_object = pyotp.TOTP(verify[2])
    system('cls')
    print("¡Good correct username and password! Now 2 factor verification")
    get_otp = input("\nInput the OTP\n[>]: ")

    return (totp_object.verify(otp = get_otp))