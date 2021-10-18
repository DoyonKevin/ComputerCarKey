import csv
import os.path

#variabe to be deleted later
drive = "/media/kevin/TESTFLASH"

#reads from the CSV file
def readCSV(drive,ledgername):
    ledgerfile = []
    with open(os.path.join(drive,ledgername),mode='r') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count !=0:
                ledgerfile.append(row)
            line_count+=1            
    return ledgerfile

#writes to a CSV file   
def writeCSV(drive,ledgername,ledgerfile):
    with open(os.path.join(drive,ledgername), mode='w') as csv_file:
        csv_writer = csv.writer(csv_file,delimiter=',', quotechar = '"', quoting = csv.QUOTE_MINIMAL, lineterminator = '\n')
        csv_writer.writerow(['Filename','Keyfile Name'])
        for row in ledgerfile:
            csv_writer.writerow(row)
    return

#parses ledger for a filename
def parseledger(ledgerfile,filename):
    filename = os.path.splitext(filename)
    for row in ledgerfile:
        #if filename is there, return filename and keyfile
        truerow = row[0]
        truerow = os.path.splitext(truerow)
        if truerow[0] == filename[0]:
            return row
    #if filename is not there, return -1
    return -1 

#adds to current ledger
def addledger(ledgerfile,filename,keyfile):
    #if file name is not in ledger
    if(parseledger(ledgerfile,filename) == -1):
        #adds filename to the ledger
        ledgerfile.append([filename,keyfile])
    return ledgerfile  

#removes from current ledger    
def delledger(ledgerfile,filename):
    x = parseledger(ledgerfile,filename)
    #If file name is there
    if(x!=-1):
        #removes from ledger
        ledgerfile.remove(x)
    return ledgerfile

# Returns True if keyname is already used
def keynameUsed(ledgerfile, keyname):
    for row in ledgerfile:
        if (keyname == row[1]):
            return True
    return False

#Genrerates ne keyfile names
def genreateKey(ledgerfile):
    key_fn = "key{}.key".format(str(len(ledgerfile)+1))
    #checks if keyfile name is in use
    if(keynameUsed(ledgerfile,key_fn)):
        count = len(ledgerfile)+2
        #continues trying new numbers until an unused one is found
        while(True):
            key_fn = "key{}.key".format(str(count)) 
            if(keynameUsed(ledgerfile,key_fn)):
               count +=1
            else:
                return key_fn
            #if too many keys have been tried, makes a problem known
            if(count>((len(ledgerfile)+1)*4)):
                key_fn = "problematic.key"
                return "Error: There was some problem generating a new key"
    #Returns new keyfile name
    return key_fn
 
if __name__ == "__main__":        
    x= readCSV(drive,"ledger.csv")
    print(x)
    y = parseledger(x,"test1.png")
    z = parseledger(x,"fake1.png")
    print(y)
    print(z)
    x = addledger(x,"test11.png",'key11.key')
    x = addledger(x,"test1.png",'key11.key')
    x = delledger(x,"test1.png")
    writeCSV(drive,'ledger.csv',x)