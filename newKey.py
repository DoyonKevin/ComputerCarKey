from subprocess import run, PIPE
from os import path,mkdir

#adds ledger and keyfile folder to drive
def createKey(drive):
    #Checks if the drive is the c drive DEFUNCT
    if(drive == "C"):
        print("C: drive cannot be a Computer Car Key")
    else:
        #Ensures the ledgerfile does not already exist DEFUNCT
        if(path.isfile(path.join(drive,"ledger.csv"))):
            print("This drive is already set up as a key!")
        else:
            #Creates new ledger file and key folder
            f1 = open(path.join(drive,"ledger.csv"),'w')
            f1.close()
            mode = 0o666
            mkdir(path.join(drive,"KeyFiles"),mode)

if __name__ == '__main__':
    createKey("D:")