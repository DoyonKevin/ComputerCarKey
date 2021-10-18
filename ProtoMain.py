from checkFlag import checkFlag
from vsnRtrv   import getPlatform, DriveInfo, rtrvDriveInfo
from CryptoFun import *
import os.path
from argparse  import ArgumentParser
from getpass   import getpass
from sys       import argv
from ledger import *
from newKey import *
from breaker import badLogic

DEBUG = 0

#filename = "image.jpg"

def _setDefaults(parser, debug):
    mode      = 0
    target_fp = None
    key_fn    = "key.key"
    hide_pwd  = False or debug

    parser.set_defaults(mode_fp=(mode, target_fp),
                        key=key_fn,
                        hide=hide_pwd
                        )
    return parser

def createParser(debug):
    parser = ArgumentParser(description="Encrypts/Decrypts file using key(s) stored on external media device.")
    parser = _setDefaults(parser, debug)
    parser = _addModeArgs(parser)
    parser.add_argument("-key", dest="key", action="store", type=str, help="Sets key name to be used.", metavar="filename")
    parser = _addHideArgs(parser)
    return parser

def _addModeArgs(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", dest="mode_fp", action="store", type=_modeEncryptFp, help="Encrypts the specified file.", metavar="filename")
    group.add_argument("-d", dest="mode_fp", action="store", type=_modeDecryptFp, help="Decrypts the specified file.", metavar="filename")
    group.add_argument("-r", dest="mode_fp", action="store", type=_modeResetFp, help="Resets password of key.", metavar="filename")
    return parser

def _modeEncryptFp(string):
    return (0, string)

def _modeDecryptFp(string):
    return (1, string)

def _modeResetFp(string):
    return (2, string)

def _modeCreateFlag(string):
    return (3, string)

def _addHideArgs(parser):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-show", dest="hide", action="store_false", help="Displays password when entered.")
    group.add_argument("-hide", dest="hide", action="store_true", help="Hides password when entered.")
    return parser

def parseArgs(args, parser, debug):
    var_dict = vars(parser.parse_args(args))

    mode_fp = var_dict["mode_fp"]
    mode = mode_fp[0]
    fp = mode_fp[1]
    key = var_dict["key"]
    hide_pwd = var_dict["hide"]

    return (mode, fp, key, hide_pwd)

def printVar(mode, fp, key, hide_pwd):
    print("--------------------------")
    print("Variable | Value")
    print("---------|-----------------")
    print("mode     | {}".format(mode))
    print("fp       | {}".format(fp))
    print("key      | {}".format(key))
    print("hide_pwd | {}".format(hide_pwd))
    print("--------------------------")       
        
def rtrvPwd(hide_pwd, prompt):
    if hide_pwd:
        return getpass(prompt)
    else:
        return input(prompt)

def rtrvFirstValidDriveVSN():
    # Search for drives with flag.txt
    sys_platform = getPlatform()
    if ("Error: " in sys_platform):
        return sys_platform
    drive_info = rtrvDriveInfo(sys_platform)
    if ("Error: " in drive_info):
        return drive_info
    drives = checkFlag(drive_info, sys_platform, "ledger.csv")
    if (len(drives) < 1):
        return "Error: Valid key is not present."
        #raise EnvironmentError("Valid key is not present. Please insert valid drive or create a valid key.")

    # Use first in list and retrieve VSN for salt
    #first_drive = pairs[0]
    #drive = first_drive[0]
    #vsn  = first_drive[1]

    # Return drive and vsn
    return drives[0]

def decryptWithChecks(filename, password, salt, drive, key_fn, ledgerfile, debug):
    if (os.path.isfile(os.path.join(drive,"KeyFiles/",key_fn))):
        if (CheckKey(password, salt, drive, ledgerfile, formatpath(filename))):
            LKey = makeKey(password,salt)
            extension = parseledger(ledgerfile,formatpath(filename))
            trueextension = os.path.splitext(extension[0])
            return decrypt(filename,LKey,trueextension[1])
        else:
            return ("Error: Incorrect Password!")
    else:
        return ("Error: No key exists!")

def encryptWithChecks(filename, password, salt, drive, key_fn, ledgerfile, debug):
    if (os.path.isfile(os.path.join(drive,"KeyFiles/",key_fn))):
        if (CheckKey(password, salt, drive, ledgerfile, formatpath(filename))):
            MKey = makeKey(password,salt)
        else:
            return ("Error: Password Incorrect!")
            #exit()
    else:
        MKey = makeKey(password,salt)
        storeKey(MKey,password,salt,drive, formatpath(filename), ledgerfile, key_fn)
    encrypt(filename, MKey)
    return "Complete"

def resetPwdWithChecks(filename, password, salt, drive, key_fn, ledgerfile, NewPass, debug):
    try:
        if (CheckKey(password, salt, drive,ledgerfile,formatpath(filename))):
            LKey = makeKey(password,salt)
            fileextention = os.path.splitext(filename)
            decryptcheck = decrypt(filename,LKey,fileextention[1])
            #NewPass = rtrvPwd(hide_pwd, "Please enter new password: ")
            MKey = makeKey(NewPass, salt)
            ledgerfile = delledger(ledgerfile,formatpath(filename))
            overwriteKey(MKey,NewPass,salt,drive, formatpath(filename), ledgerfile, key_fn)
            encrypt(filename, MKey)
            return "Complete"
        else:
            return ("Error: Incorrect Password! Can't replace current key!")
    except:
        return ("Error: No Key to replace!")

def main2(pwd, mode, fp, newpwd="password",key="key.key"):

    drive_info = rtrvFirstValidDriveVSN()
    if isinstance(drive_info, str):
        if ("Error: " in drive_info):
            return drive_info
        
    if DEBUG:
        print("Salt: {}".format(drive_info.getVSN()))
    
    ledgername = "ledger.csv"

    if (os.path.isfile(os.path.join(drive_info.getPath(),ledgername))!=True):
        createKey(drive_info.getPath())

    ledgerfile = readCSV(drive_info.getPath(),ledgername)
    parsedkey = parseledger(ledgerfile,formatpath(fp))

    key = genreateKey(ledgerfile)

    if(key == "Error: There was some problem generating a new key"):
        return key

    if(parsedkey != -1):
        key = parsedkey[1]
    
    check = badLogic(fp,ledgerfile,drive_info.getPath(),pwd,newpwd)
    if( check != "good"):
        return check

    # Encryption
    if (mode == 0):
        returnencrypt = encryptWithChecks(fp, pwd, drive_info.getVSN(), drive_info.getPath(), key, ledgerfile, DEBUG)
        return returnencrypt
    # Decryption
    elif (mode == 1):
        returndecrypt = decryptWithChecks(fp, pwd, drive_info.getVSN(), drive_info.getPath(), key, ledgerfile, DEBUG)
        return returndecrypt
    # Reset Password
    elif (mode == 2):
        returnreset = resetPwdWithChecks(fp, pwd, drive_info.getVSN(), drive_info.getPath(), key, ledgerfile, newpwd, DEBUG)
        return returnreset
    else:
        parser.print_help()
        return

def _main(password, arg, filename):

    # Search for drives with flag.txt
    pairs = checkFlag(rtrvDriveVSNPairs(getPlatform()), getPlatform(), "flag.txt")
    if (len(pairs) < 1):
        print("Valid key is not present.")
        return

    # Use first in list and retrieve VSN for salt
    first_drive = pairs[0]
    drive = first_drive[0]
    salt  = first_drive[1]
    if DEBUG:
        print(salt)

    # Retrieve password
    # password = input("Please insert password:  ")

    
    # for arg in argv[1::]: # argv[0] will always be crypto.py

    if arg == "-d":
        if (os.path.isfile(os.path.join(drive,"key.key"))):
            if (CheckKey(password, salt, drive)):
                LKey = makeKey(password,salt)
                decrypt(filename,LKey)
            else:
                print ("Incorrect Password!\n")
        else:
            print ("No key exists!")

    elif arg == "-e":
        if (os.path.isfile(os.path.join(drive,"key.key"))):
            if (CheckKey(password, salt, drive)):
                MKey = makeKey(password,salt)
            else:
                print ("Password Incorrect!\n")
                exit()
        else:
            MKey = makeKey(password,salt)
            storeKey(MKey,password,salt,drive)
        encrypt(filename, MKey)

    elif arg == "-r":
        try:
            if (CheckKey(password, salt, drive)):
                LKey = makeKey(password,salt)
                decrypt(filename,LKey)

                NewPass = input("Type in new password:   ")
                MKey = makeKey(NewPass, salt)
                storeKey(MKey,NewPass,salt,drive)
                encrypt(filename, MKey)
            else:
                print ("Incorrect Password! Can't replace current key!")
        except:
            print ("No Key to replace!")

    else:
        print ("Invalid flag, try -e, -d, or -r")

if __name__ == "__main__":
    parser = createParser(DEBUG)
    (mode, fp, key, hide_pwd) = parseArgs(argv[1:], parser, DEBUG)
    pwd = rtrvPwd(hide_pwd, "Please enter password: ")
    
    if DEBUG:
        printVar(mode, fp, key, hide_pwd)
    
    main2(pwd, mode, fp, key)