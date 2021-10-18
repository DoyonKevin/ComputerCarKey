import os.path
from CryptoFun import formatpath
from ledger import parseledger

#checks to see if the following errors occurs, returns error if it does
def badLogic(filepath,ledgerfile,drive,password,newpwd):
    #if file is actually a folder
    if(os.path.isdir(filepath)):
        return "Error: Folders can not be encrypted. Please give a file"
        #return True
    #if file does not exist
    if(os.path.isfile(filepath)!=True):
        return "Error: File does not exist"
        #return True
    filename = formatpath(filepath)
    #if the filename is actually ledger
    if(filename == "ledger.csv"):
        return "Error: ledger.csv cannot be encrypted. DO NOT encrypt your ledger file."
        #return True
    keyfile = parseledger(ledgerfile,filename)
    #If there is a key file in the ledger
    if(keyfile != -1):
        keyfile = keyfile[1]
        #But the keyfile does not actually exist
        if(os.path.isfile(os.path.join(drive,"KeyFiles",keyfile))!=True):
            return "Error: Keyfile listed in ledger does not exist"
            #return True
    return "good"