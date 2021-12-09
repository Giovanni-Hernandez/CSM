import pyotp

#import qrcode
def verificate_otp(username):
    file1 = open("../CSM/users/"+username, "r")
    verify = file1.read().splitlines()
    file1.close()
    totp_object = pyotp.TOTP(verify[2])

   # qr_text = totp_object.provisioning_uri(name=username, issuer_name="CSM Security Master")

    get_otp = input("Ingresa el OTP: ")

    return (totp_object.verify(otp = get_otp))

