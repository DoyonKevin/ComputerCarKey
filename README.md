# ComputerCarKey

This repository is a recreation of a repository I previously worked on with Scott Young, Dawson Markham, and Benjammin Hargrove
This repository is better organized than the original, and has several redundant or unneeded files removed. Only files needed for the project remain.

The original repository can be found here: https://github.com/scotty2hottie98/CYEN_Senior_Design

Computer Car Keys is a project intended to help users protect their files by using 2FA and encryption.
When using Computer Car Keys, users will be prompted for serveral things including which file they wish to encrypt/decrypt, an external media device(such as a USB drive, for verification), and the password associated with that file

If the password is correct and users have the corresponding USB device used when creating the password, the file will encrypt/decrypt

# Running the program

To run Computer Car Keys you can either run the provided executable, or run MainGUI.py. The included GUI will assist users in operating the program.

# NOTES

The module "cryptography" is required to run this program with MainGUI.py. It can be obtained with "pip install cryptography." "Cryptography" is not needed when using the executable.

When the program is run, users must have the USB drive they wish to use already plugged into their computer.

This program cannot be tun without the provided .ico file.
