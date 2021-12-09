#Generar un factor de autentificación en 2 pasos
import pyotp
import qrcode

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
