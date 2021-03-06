import rsa


# Generates public and private RSA keys
def generateRSAKeys():
    (pubKey, privKey) = rsa.newkeys(2048)

    return (pubKey, privKey)


# Saves either public or private RSA keys
def saveRSAKey(route, filename, key):
    with open(route + filename + '.pem', 'wb') as f:
        f.write(key.save_pkcs1('PEM'))


# Reads RSA private key
def readRSAPrivateKey(route, filename):
    with open(route + filename + '.pem', 'rb') as f:
        privKey = rsa.PrivateKey.load_pkcs1(f.read())

    return privKey


# Reads RSA public key
def readRSAPublicKey(route, filename):
    with open(route + filename + '.pem', 'rb') as f:
        pubKey = rsa.PublicKey.load_pkcs1(f.read())

    return pubKey


# Encrypts data using RSA
def encryptRSA(msgBytes, key):
    return rsa.encrypt(msgBytes, key)


# Decrypts data using RSA
def decryptRSA(cipherBytes, key):
    try:
        return rsa.decrypt(cipherBytes, key)
    except:
        return False


# Signs data using SHA-256
def signSHA256(msgBytes, key):
    return rsa.sign(msgBytes, key, 'SHA-256')


# Verifies signatures using SHA-256
def verifySHA256(msgBytes, signature, key):
    try:
        return rsa.verify(msgBytes, signature, key) == 'SHA-256'
    except:
        return False
