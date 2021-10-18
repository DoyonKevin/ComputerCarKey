from subprocess import run, PIPE

# Return bytestring as ASCII text without leading and trailing whitespace
def _cleanStdout(byte_string):
    return byte_string.decode("ASCII").rstrip().lstrip()

# Return encoded string from command
def _runCmdList(cmd_list, isShellCmd=False):
    process = run(cmd_list, stdout=PIPE, shell=isShellCmd)
    return _cleanStdout(process.stdout)

def winQuickFormatDrive(drive_name, vol_name=""):
    if (drive_name == "C:"):
        return "Error: Unable to format C: drive."
        #raise OSError("Cannot reformat C: drive.")
    cmd = ["format", drive_name, "/FS:FAT32", "/V:"+vol_name, "/Q"]
    process = run(cmd, stdin=PIPE, shell=True)
    return "Format completed."

def linQuickFormatDrive(drive_name, vol_name=""):
    cmd_list1 = ["umount", drive_name]
    cmd_list2 = ["mkfs.vfat", drive_name]
    if (vol_name != ""):
        cmd_list2 += ["-n", vol_name]
    _runCmdList(cmd_list1)
    _runCmdList(cmd_list2)
    return "Format completed."

def quickFormatDrive(drive_name, vol_name="", plat="win"):
    if (plat == "win"):
        return winQuickFormatDrive(drive_name, vol_name)
    elif (plat == "lin"):
        return linQuickFormatDrive(drive_name, vol_name)
    else:
        return "Error: Unsupported platform."
        #raise ValueError("Unexpected platform string...")

# quickFormatDrive("/dev/sdb1", vol_name="", plat="lin")