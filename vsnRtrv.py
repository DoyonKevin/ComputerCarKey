#############
# LIBRARIES #
############################################################################################\
from subprocess import run, PIPE
from sys import platform
############################################################################################/

#############
#  CLASSES  #
############################################################################################\

# Creates a class that stores a drive's name, vsn and path
class DriveInfo:

    # Initialize instance -------------------------------------------------------------------
    def __init__(self, drive, vsn, path):
        self._drive = drive
        self._path  = path
        self._vsn   = vsn
    # ---------------------------------------------------------------------------------------

    # String --------------------------------------------------------------------------------
    def __str__(self):
        return self._drive

    def printinfo(self):
        return "Drive: {}, Path: {}, VSN: {}".format(self._drive, self._path, self._vsn)

    # ---------------------------------------------------------------------------------------

    # Accessors/Mutators --------------------------------------------------------------------
    def getDrive(self):
        return self._drive

    def setDrive(self, drive):
        self._drive = drive

    def getPath(self):
        return self._path

    def setPath(self, path):
        self._path = path
        
    def getVSN(self):
        return self._vsn

    def setVSN(self, vsn):
        self._vsn = vsn
    # ---------------------------------------------------------------------------------------

    # Update (Use after formatting) ---------------------------------------------------------
    # TOO BE ADDED IF NEEDED
    def updateInfo(self):
        return
    
    def updatePath(self):
        return

    def updateVSN(self):
        return
    # ---------------------------------------------------------------------------------------

############################################################################################/

#############
# FUNCTIONS #
############################################################################################\

# Utilities ---------------------------------------------------------------------------------

# Return string representing system type (also provides check against unknown platforms)
def getPlatform():
    if "linux" in platform:
        return "lin"
    elif (platform == "win32"):
        return "win"
    else:
        return "Error: Unsupported platform."
        #print("PlatformError: This platform is not supported")
        #exit()

# Return bytestring as ASCII text without leading and trailing whitespace
def _cleanStdout(byte_string):
    return byte_string.decode("ASCII").rstrip().lstrip()

# Return encoded string from command
def _runCmdList(cmd_list, isShellCmd=False):
    process = run(cmd_list, stdout=PIPE, shell=isShellCmd)
    return _cleanStdout(process.stdout)

# Info Retrieval -----------------------------------------------------------------------------

# Return list of drives' info with function corresponding to system type
def rtrvDriveInfo(sys_type="win"):
    if (sys_type == "lin"):
        drive_info_list = rtrvDrivesInfoLinux()
        return _convDrivesInfoListToClassLinux(drive_info_list)
    elif (sys_type == "win"):
        drive_info_list = rtrvDriveVSNPairsWindows()
        return _convDrivesInfoListToClassWindows(drive_info_list)
    else:
        #raise ValueError("Unexpected system type argument...")
        return "Error: Unsupported platform."

# Linux ----------------------------------------------------------------------------

# Return dirves' info on a linux system
def rtrvDrivesInfoLinux():
    # Run command
    cmd_list = ["blkid"]
    rtrn_str = _runCmdList(cmd_list)
    # Split string into lines
    lines    = rtrn_str.split("\n")
    # Split lines into elements
    lines_split = []
    for line in lines:
        lines_split.append(line.split())
    # Parse lines for drive/uuid pairs
    drive_vsn_pairs = []
    for line_split in lines_split:
        for element in line_split:
            if (("UUID=" in element) and not ("PARTUUID=" in element)):
                drive = line_split[0]
                uuid  = element[6:-1]
                if (len(uuid) > 9 and len(uuid) < 17):
                    uuid = uuid[8:12] + "-" + uuid[12:]
                if not ("sda" in drive):
                    drive_vsn_pairs.append([drive[:-1], uuid])
    # Append path to mounted drives
    drives_info = addDrivesPathsLinux(drive_vsn_pairs)
    # Return drive info
    return drives_info

# Returns list with paths appended to each entry
def addDrivesPathsLinux(drive_vsn_pairs):
    # Make copy of list
    pairs = drive_vsn_pairs.copy()
    # Run command
    cmd_list = ["df", "-h"]
    output   = _runCmdList(cmd_list)
    lines    = output.split("\n")
    # Search for each drive name on each line
    for i in range(0, len(pairs)):
        for line in lines:
            if pairs[i][0] in line:
                split = line.split(" ")
                pairs[i].append(split[-1])
    # Return new list (Pairs is now a misnomer)
    return pairs

# Windows --------------------------------------------------------------------------

# Return the pairs on a Windows system 
def rtrvDriveVSNPairsWindows():
    # Retrieve drive names and VSNs
    drives = rtrvDriveListWindows()
    vsns   = rtrvDriveListVSNsWindows(drives)
    # Create pairs
    drive_vsn_pairs = []
    for i in range(0,len(drives)):
        drive_vsn_pairs.append([drives[i], vsns[i]])
    return drive_vsn_pairs

# Return list of drives on a Windows system
def rtrvDriveListWindows():
    # Run command
    cmd_list  = ["fsutil", "fsinfo", "drives"]
    rtrn_str  = _runCmdList(cmd_list)
    # Parse string
    rtrn_list = rtrvDrivesFromStrWindows(rtrn_str)
    # Return list
    return rtrn_list

# Return parallel list of VSNs
def rtrvDriveListVSNsWindows(drive_list):
    # Create parallel list
    rtrn_list = []
    for drive in drive_list:
        rtrn_list.append(rtrvDriveVSNWindows(drive))
    # Return list
    return rtrn_list

# Return VSN of Drive
def rtrvDriveVSNWindows(drive):
    # Run command and return parsed output
    cmd_list = ["vol", drive]
    vsn_str  = _runCmdList(cmd_list, True)
    return rtrvVSNFromStrWindows(vsn_str)

# Parses drive list from string (Windows)
def rtrvDrivesFromStrWindows(string):
    rtrn_list = []
    # Divide string
    split_str = string.split()
    # Add drives
    for i in range(1,len(split_str)):
        rtrn_list.append(split_str[i][:-1])
    # Return list
    return rtrn_list

# Returns VSN from string (Windows)
def rtrvVSNFromStrWindows(string):
    split_str = string.split()
    return split_str[-1]

# Private -----------------------------------------------------------------------------------

# Functions convert list containing drive info into a class containing drive info
# Linux Version (path != name)
def _convDrivesInfoListToClassLinux(info_list):
    class_list = []
    for info in info_list:
    	if (len(info[1]) <= 9):
            class_list.append(DriveInfo(info[0], info[1], info[2]))
    return class_list
# Windows version (path == name)
def _convDrivesInfoListToClassWindows(info_list):
    class_list =[]
    for info in info_list:
        class_list.append(DriveInfo(info[0], info[1], info[0]))
    return class_list

# Deprecated --------------------------------------------------------------------------------

# Return the pairs generated by the function corresponding to system type
#def rtrvDriveVSNPairs(sys_type="win"):
#    if (sys_type == "lin"):
#        return rtrvDriveVSNPairsLinux()
#    else:
#        return rtrvDriveVSNPairsWindows()

# Return the pairs on a linux system (NOTE: may include more than VSNs)
#def rtrvDriveVSNPairsLinux():
    # Run command
#    cmd_list = ["blkid"]
#    rtrn_str = _runCmdList(cmd_list)
    # Split string into lines
#    lines    = rtrn_str.split("\n")
    # Split lines into elements
#    lines_split = []
#    for line in lines:
#        lines_split.append(line.split())
    # Parse lines for drive/uuid pairs
#    drive_vsn_pairs = []
#    for line_split in lines_split:
#        for element in line_split:
#            if (("UUID=" in element) and not ("PARTUUID=" in element)):
#                drive_vsn_pairs.append([line_split[0], element[6:-1]])
    # Return pairs
#    return drive_vsn_pairs

############################################################################################/

#############
#   MAIN    #
############################################################################################\
def _main():
    infos = rtrvDriveInfo(getPlatform())
    for info in infos:
        print(info.printinfo())

if (__name__ == "__main__"):
    _main()
############################################################################################/