import base64, hashlib
from sys import argv, stderr
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os.path
from ledger import *

DEBUG = 0

#Generates keys based on password and VSN
def makeKey(password,salt):
    VSN = salt.encode("utf-8")
    backend=default_backend()
    #Key derivation function with VSN as salt
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=VSN,iterations=10000,backend=backend)

    #Encodes in base 64 to work with encryption algorithm
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    #returns the key
    return key

#Decrypts files
def decrypt(filename,key,extension=".txt"):
    try:
        #setting up decryption
        f = Fernet(key)
        #Reads file to be decrypted
        with open(filename, "rb") as file_name:
            token = file_name.read()
        #Decrypts file
        d = f.decrypt(token)
        #Write decrypted info back in original file name
        with open(filename,"wb") as file_name:
            file_name.write(d)
        #Changes file extension back to original file extenstion
        pre = os.path.splitext(filename)
        os.rename(filename,pre[0]+extension)
        return "Complete"
    except:
        return "Error: This is already Decrypted!"

#Encrypts files
def encrypt(filename,key):
    #Sets up encryption
    f = Fernet(key)
    #Reads file to be encrypted
    with open(filename, "rb") as file_name:
        plaintext = file_name.read()
    #encrypts file information
    token = f.encrypt(plaintext)
    #Writes encrypted info to original file name
    with open(filename,"wb") as file_name:
        file_name.write(token)
    #Changes file extenstion to .cck
    pre = os.path.splitext(filename)
    os.rename(filename, pre[0] + ".cck")

#Reads key from the Computer Car Key
def loadKey(drive,ledgerfile,filename):
    parsedinfo = parseledger(ledgerfile,filename)
    if(parsedinfo!=-1):
        return open(os.path.join(drive,"KeyFiles",parsedinfo[1]),"rb").read()
    else:
        return False

 #Checks if the loaded key, and the key generated from the password/salt are the same       
def CheckKey(password,salt, drive,ledgerfile,filename):
    # Load the current Existing Key
    CorrectKey = loadKey(drive,ledgerfile,filename)
    if(CorrectKey==False):
        return False
    # First Stage to creating a key, using key derivation functions
    VSN = salt.encode("utf-8")
    backend=default_backend()
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=VSN,iterations=10000,backend=backend)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    #Debug the key comparison
    if (DEBUG == 1):
        print(CorrectKey)
        print(key)
    #Second stage to making new key, using a new key derivation function
    kdf2=Scrypt(salt=VSN,length=32,n=2**14,r=8,p=1,backend=backend)
    key = base64.urlsafe_b64encode(kdf2.derive(key))
    # Debug they key comparison
    if (DEBUG == 1):
        print (CorrectKey)
        print (key)
    # Compare the Keys
    if (CorrectKey == key):
        return True
    else:
        return False

#makes key able to be safely stored
def storeKey(key,password,salt,drive,filename,ledgerfile,keyfile):
    #Encryts the usable key with a new key derivation function
    VSN = salt.encode("utf-8")
    backend = default_backend()
    kdf2=Scrypt(salt=VSN,length=32,n=2**14,r=8,p=1,backend=backend)
    key = base64.urlsafe_b64encode(kdf2.derive(key))
    #Ensures key name has not been used
    if(keynameUsed(ledgerfile,keyfile)):
        print("Key File Name Has Been Used")
    #Writes new key info to approrptiate place
    else:
        with open(os.path.join(drive,"KeyFiles",keyfile),"wb") as key_file:
            key_file.write(key)
            key_file.close()
        ledgerfile = addledger(ledgerfile,str(filename),str(keyfile))
        writeCSV(drive,"ledger.csv",ledgerfile)

#When replacing keys, overwrites the orignal key file
def overwriteKey(key,password,salt,drive,filename,ledgerfile,keyfile):
    #encrypts the usable key with a new key derivation function
    VSN = salt.encode("utf-8")
    backend = default_backend()
    kdf2=Scrypt(salt=VSN,length=32,n=2**14,r=8,p=1,backend=backend)
    key = base64.urlsafe_b64encode(kdf2.derive(key))
    #Stores key in the appropriate place
    with open(os.path.join(drive,"KeyFiles",keyfile),"wb") as key_file:
        key_file.write(key)
        key_file.close()

#so we can get filepath for encrypt/decrypt and use it for loadkey/storekey    
def formatpath(filename):
    filename = os.path.split(filename)
    filename = filename[-1]
    return filename