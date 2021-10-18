#from vsnRtrv import rtrvDriveVSNPairs, getPlatform
import os
from subprocess import run, PIPE

# Return bytestring as ASCII text without leading and trailing whitespace
def _cleanStdout(byte_string):
    return byte_string.decode("ASCII").rstrip().lstrip()
    
# Return encoded string from command
def _runCmdList(cmd_list, isShellCmd=False):
    process = run(cmd_list, stdout=PIPE, shell=isShellCmd)
    return _cleanStdout(process.stdout)

def checkFlag(drive_infos, platform="win",flag="flag.txt"):
    valid_drives = []
    for info in drive_infos:
        if os.path.isfile(os.path.join(info.getPath(), flag)):
            valid_drives.append(info)
    return valid_drives


####################### MAIN #########################################

if __name__ == "__main__":
    pairs = checkFlag(rtrvDriveVSNPairs(getPlatform()), getPlatform())
    for pair in pairs:
        print("Drive: {}\tVSN: {}".format(pair[0], pair[1]))