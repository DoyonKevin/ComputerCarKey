from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from ProtoMain import *
from formatDrive import *
from newKey import *
from vsnRtrv import *
from os.path import expanduser

##### Production Functions #####

def MainClick(process):
    if (process == "Encrypt"):
        MainGUI.destroy()
        EncryptGuiSetup()
    elif (process == "Decrypt"):
        MainGUI.destroy()
        DecryptGuiSetup()
    elif (process == "Password Change"):
        MainGUI.destroy()
        PasswordGUISetup()
    elif (process == "New Key"):
        MainGUI.destroy()
        NewKeyGUISetup()

def EncryptClick(process):
    # Clear Error Handeling Label
    label3 = Label(EncryptGUI, text = "                                                    ", bg = "#f6f6f6")
    label3.grid(row = 5, column = 1, columnspan = 4)
    label3.pack_propagate(0) # don't shrink

    if (process == "Back"):
        EncryptGUI.destroy()
        MainGuiSetup()
    elif (process == "Encrypt"):
        error = main2(passentry.get(), int(0), fileentry.get())
        # Error Handeling messaging 
        if (error == "Complete"):
            label3 = Label(EncryptGUI, text = "Encryption Successful!", bg = "#f6f6f6", fg = "Green")
            label3.grid(row = 5, column = 1, columnspan = 4)
            label3.pack_propagate(0) # don't shrink
        else:
            label3 = Label(EncryptGUI, text = error, bg = "#f6f6f6", fg = "red")
            label3.grid(row = 5, column = 1, columnspan = 4)
            label3.pack_propagate(0) # don't shrink
    else:
        label3 = Label(EncryptGUI, text = "Something Went Wrong", bg = "#f6f6f6", fg = "purple")
        label3.grid(row = 5, column = 1, columnspan = 4)
        label3.pack_propagate(0) # don't shrink

def DecryptClick(process):
    # Clear Error Handeling Label
    label3 = Label(DecryptGUI, text = "                                                    ", bg = "#f6f6f6")
    label3.grid(row = 5, column = 1, columnspan = 4)
    label3.pack_propagate(0) # don't shrink

    if (process == "Back"):
        DecryptGUI.destroy()
        MainGuiSetup()
    elif (process == "Decrypt"):
        error = main2(passentry.get(), 1, fileentry.get())
        if (error == "Complete"):
            label3 = Label(DecryptGUI, text = "Decrypt Complete!", bg = "#f6f6f6", fg = "Green")
            label3.grid(row = 5, column = 1, columnspan = 4)
            label3.pack_propagate(0) # don't shrink
        else:
            label3 = Label(DecryptGUI, text = error, bg = "#f6f6f6", fg = "Red")
            label3.grid(row = 5, column = 1, columnspan = 4)
            label3.pack_propagate(0) # don't shrink
    else:
        label3 = Label(DecryptGUI, text = "Something Broke", bg = "#f6f6f6")
        label3.grid(row = 5, column = 1, columnspan = 4)
        label3.pack_propagate(0) # don't shrink

def PassClick(process):
    # Blank Error Label
    ErrorLabel = Label(PassGUI, text = "                                                                                                                 ", pady = 30, bg = "#f6f6f6")
    ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
    ErrorLabel.pack_propagate(0) # don't shrink

    if (process == "Back"):
        PassGUI.destroy()
        MainGuiSetup()
    elif (process == "Replace"):
        if (entry1.get() != entry2.get()):
            if (entry2.get() == entry3.get()):
                error = main2(entry1.get(), 2, fileentry.get(), entry2.get())
                if (error == "Complete"):
                    ErrorLabel = Label(PassGUI, text = "Password Changed Successfully!", pady = 30, bg = "#f6f6f6", fg = "Green")
                    ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
                    ErrorLabel.pack_propagate(0) # don't shrink
                else:
                    ErrorLabel = Label(PassGUI, text = error, pady = 30, bg = "#f6f6f6", fg = "Red")
                    ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
                    ErrorLabel.pack_propagate(0) # don't shrink
            else:
                ErrorLabel = Label(PassGUI, text = "New Passwords Do Not Match!", pady = 30, bg = "#f6f6f6", fg = "red")
                ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
                ErrorLabel.pack_propagate(0) # don't shrink
        else:
            ErrorLabel = Label(PassGUI, text = "New Password Cannot be the Same as Old Password!", pady = 30, bg = "#f6f6f6", fg = "red")
            ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
            ErrorLabel.pack_propagate(0) # don't shrink

def NewKeyClick(process):

    label2 = Label(KeyGUI, text = "                                                                  ", bg = "#f6f6f6")
    label2.grid(row = 4, column = 2, columnspan = 3)
    label2.pack_propagate(0) # don't shrink

    if (process == "Back"):
        KeyGUI.destroy()
        MainGuiSetup()
    elif (process == "Launch"):
        if (Combo.get() == "No Valid Drives Found" or Combo.get() == "Pick an Option"):
            label2 = Label(KeyGUI, text = "Invalid Drive", bg = "#f6f6f6", fg = "Red")
            label2.grid(row = 4, column = 2, columnspan = 3)
            label2.pack_propagate(0) # don't shrink
        else:
            error = quickFormatDrive(Combo.get(), nameentry.get().upper(), getPlatform())
            
            drive_path = Combo.get()
            canCreate = True
            if (getPlatform() != "win"):
                warning = messagebox.showinfo("Continue?", "Please remove drive and reinsert before continuing.")
                drives = rtrvDriveInfo(getPlatform())
                canCreate = False
                for drive in drives:
                    if drive.getDrive() == Combo.get():
                        drive_path = drive.getPath()
                        canCreate = True
                        break
            if canCreate:
                createKey(drive_path)

            if not canCreate:
                label2 = Label(KeyGUI, text = "Error: Unable to determine path.", bg = "#f6f6f6", fg = "red")
                label2.grid(row = 4, column = 2, columnspan = 3)
                label2.pack_propagate(0) # don't shrink

            elif (error == "Format completed."):
                label2 = Label(KeyGUI, text = "Formatted Successfully!", bg = "#f6f6f6", fg = "Green")
                label2.grid(row = 4, column = 2, columnspan = 3)
                label2.pack_propagate(0) # don't shrink
            else:
                label2 = Label(KeyGUI, text = error, bg = "#f6f6f6", fg = "red")
                label2.grid(row = 4, column = 2, columnspan = 3)
                label2.pack_propagate(0) # don't shrink

def GetFilePath():
    currentuser = expanduser("~")
    path = filedialog.askopenfilename(initialdir=currentuser, title="Select file",
                    filetypes=(("all files", "*.*"),("txt files", "*.txt")))

    fileentry.delete(0, END)
    fileentry.insert(0, str(path))

    # Debug how the file path displays
    # print ("\nThe file path is '{}' \n".format(path))
    
# GUI Functions

def MainGuiSetup():

    global MainGUI

    MainRunning = 0

    #### GUI Setup ###
    MainGUI = Tk()
    MainGUI.title("Computer Car Keys")
    MainGUI.geometry("1000x600+50+50")
    MainGUI.configure(bg = "#f6f6f6")
    if (getPlatform() == "win"):
        MainGUI.iconbitmap(r'CarKeyIcon.ico')

    ### Button and Text Propogation ###

    labelfill1 = Label(MainGUI, text = " ", padx = 5, bg = "#f6f6f6")
    labelfill1.grid(row = 0, column = 0, columnspan = 1, rowspan = 4)
    labelfill1.pack_propagate(0) # don't shrink

    Label1Text = "Welcome to Computer Car Key Management Tool! \nPlease select one of the options to begin."
    label1 = Label(MainGUI, text = Label1Text, padx = 225, pady = 225, bg = "#f6f6f6", font=("Comic Sans", 14))
    label1.grid(row = 0, column = 1, columnspan = 5)
    label1.pack_propagate(0) # don't shrink

    button1 = Button(MainGUI, text = "Encrypt", command = lambda: MainClick("Encrypt"), padx = 15, pady = 15, bg = "#f6f6f6")
    button1.grid(row = 1, column = 1, columnspan = 1)
    button1.pack_propagate(0)

    button2 = Button(MainGUI, text = "Decrypt", command = lambda: MainClick("Decrypt"), padx = 15, pady = 15, bg = "#f6f6f6")
    button2.grid(row = 1, column = 3, columnspan = 1)
    button2.pack_propagate(0)

    button3 = Button(MainGUI, text = "Password Change", command = lambda: MainClick("Password Change"), padx = 15, pady = 15, bg = "#f6f6f6")
    button3.grid(row = 1, column = 5, columnspan = 3)
    button3.pack_propagate(0)

    labelfill2 = Label(MainGUI, text = " ", bg = "#f6f6f6")
    labelfill2.grid(row = 2, column = 1, columnspan = 5)
    labelfill2.pack_propagate(0) # don't shrink

    button4 = Button(MainGUI, text = "New Key", command = lambda: MainClick("New Key"), fg = "blue")
    button4.grid(row = 3, column = 3, columnspan = 1)
    button4.pack_propagate(0)
    
    MainGUI.mainloop()

def EncryptGuiSetup():

    global EncryptGUI, passentry, fileentry, label3

    EncryptGUI = Tk()
    EncryptGUI.title("Computer Car Keys: Encrypting")
    EncryptGUI.geometry("1000x600+50+50")
    EncryptGUI.configure(bg = "#f6f6f6")
    if (getPlatform() == "win"):
        EncryptGUI.iconbitmap(r'CarKeyIcon.ico')

    # All of the Fill layers

    labelfill1 = Label(EncryptGUI, text = " ", padx = 50, bg = "#f6f6f6")
    labelfill1.grid(row = 0, column = 0, columnspan = 1, rowspan = 5)
    labelfill1.pack_propagate(0) # don't shrink

    labelfill2 = Label(EncryptGUI, text = " ", pady = 5, bg = "#f6f6f6")
    labelfill2.grid(row = 0, column = 1, columnspan = 4)
    labelfill2.pack_propagate(0) # don't shrink

    labelfill3 = Label(EncryptGUI, text = " ", pady = 5, bg = "#f6f6f6")
    labelfill3.grid(row = 3, column = 1, columnspan = 4)
    labelfill3.pack_propagate(0) # don't shrink

    # All functioning layers

    label1 = Label(EncryptGUI, text = "Please Input File Path to Encrypt", padx = 250, pady = 75, bg = "#f6f6f6", font=("Comic Sans", 14))
    label1.grid(row = 1, column = 1, columnspan = 4)
    label1.pack_propagate(0) # don't shrink

    fileentry = Entry(EncryptGUI, width = 100, fg="Black")
    fileentry.grid(row = 2, column = 1, columnspan = 4)
    fileentry.pack_propagate(0) # don't shrink

    filebutton = Button(EncryptGUI, text = "...", command = GetFilePath, bg = "#f6f6f6")
    filebutton.grid(row = 2, column = 5)
    filebutton.pack_propagate(0) # don't shrink

    label2 = Label(EncryptGUI, text = "Password:", pady = 25, bg = "#f6f6f6", font=("Comic Sans", 11))
    label2.grid(row = 4, column = 1)
    label2.pack_propagate(0) # don't shrink

    passentry = Entry(EncryptGUI, width = 63, show = "*")
    passentry.grid(row = 4, column = 2, columnspan = 3)
    passentry.pack_propagate(0) # don't shrink

    label3 = Label(EncryptGUI, text = "                                            ", bg = "#f6f6f6")
    label3.grid(row = 5, column = 1, columnspan = 4)
    label3.pack_propagate(0) # don't shrink

    button1 = Button(EncryptGUI, text = "Encrypt", command = lambda: EncryptClick("Encrypt"), padx = 15, pady = 15, bg = "#f6f6f6")
    button1.grid(row = 6, column = 4)
    button1.pack_propagate(0)

    button2 = Button(EncryptGUI, text = "Back", command = lambda: EncryptClick("Back"), padx = 15, pady = 15, bg = "#f6f6f6")
    button2.grid(row = 6, column = 1)
    button2.pack_propagate(0)

    EncryptGUI.mainloop()

def DecryptGuiSetup():

    global DecryptGUI, passentry, fileentry, label3

    DecryptGUI = Tk()
    DecryptGUI.title("Computer Car Keys: Decrypting")
    DecryptGUI.geometry("1000x600+50+50")
    DecryptGUI.configure(bg = "#f6f6f6")
    if (getPlatform() == "win"):
        DecryptGUI.iconbitmap(r'CarKeyIcon.ico')

    # All of the Fill layers

    labelfill1 = Label(DecryptGUI, text = " ", padx = 50, bg = "#f6f6f6")
    labelfill1.grid(row = 0, column = 0, columnspan = 1, rowspan = 5)
    labelfill1.pack_propagate(0) # don't shrink

    labelfill2 = Label(DecryptGUI, text = " ", pady = 5, bg = "#f6f6f6")
    labelfill2.grid(row = 0, column = 1, columnspan = 4)
    labelfill2.pack_propagate(0) # don't shrink

    labelfill3 = Label(DecryptGUI, text = " ", pady = 5, bg = "#f6f6f6")
    labelfill3.grid(row = 3, column = 1, columnspan = 4)
    labelfill3.pack_propagate(0) # don't shrink

    # All functioning layers

    label1 = Label(DecryptGUI, text = "Please Input File Path to Decrypt", padx = 250, pady = 75, bg = "#f6f6f6", font=("Comic Sans", 14))
    label1.grid(row = 1, column = 1, columnspan = 4)
    label1.pack_propagate(0) # don't shrink

    fileentry = Entry(DecryptGUI, width = 100, fg="Black")
    fileentry.grid(row = 2, column = 1, columnspan = 4)
    fileentry.pack_propagate(0) # don't shrink

    filebutton = Button(DecryptGUI, text = "...", command = GetFilePath, bg = "#f6f6f6")
    filebutton.grid(row = 2, column = 5)
    filebutton.pack_propagate(0) # don't shrink

    label2 = Label(DecryptGUI, text = "Password:", pady = 25, bg = "#f6f6f6", font=("Comic Sans", 11))
    label2.grid(row = 4, column = 1)
    label2.pack_propagate(0) # don't shrink

    passentry = Entry(DecryptGUI, width = 63, show = "*")
    passentry.grid(row = 4, column = 2, columnspan = 3)
    passentry.pack_propagate(0) # don't shrink

    label3 = Label(DecryptGUI, text = "                                                 ", bg = "#f6f6f6")
    label3.grid(row = 5, column = 1, columnspan = 4)
    label3.pack_propagate(0) # don't shrink

    button1 = Button(DecryptGUI, text = "Decrypt", command = lambda: DecryptClick("Decrypt"), padx = 15, pady = 15, bg = "#f6f6f6")
    button1.grid(row = 6, column = 4)
    button1.pack_propagate(0)

    button2 = Button(DecryptGUI, text = "Back", command = lambda: DecryptClick("Back"), padx = 15, pady = 15, bg = "#f6f6f6")
    button2.grid(row = 6, column = 1)
    button2.pack_propagate(0)

    DecryptGUI.mainloop()

def PasswordGUISetup():

    global PassGUI, entry1, entry2, entry3, fileentry, ErrorLabel

    PassGUI = Tk()
    PassGUI.title("Computer Car Keys: Password Reset")
    PassGUI.geometry("1000x600+50+50")
    PassGUI.configure(bg = "#f6f6f6")
    if (getPlatform() == "win"):
        PassGUI.iconbitmap(r'CarKeyIcon.ico')

    # All of the Fill layers

    labelfill1 = Label(PassGUI, text = " ", padx = 50, bg = "#f6f6f6")
    labelfill1.grid(row = 0, column = 0, rowspan = 6)
    labelfill1.pack_propagate(0) # don't shrink

    labelfill2 = Label(PassGUI, text = " ", padx = 50, bg = "#f6f6f6")
    labelfill2.grid(row = 0, column = 1, columnspan = 5)
    labelfill2.pack_propagate(0) # don't shrink

    # All functioning layers

    titleLabel = Label(PassGUI, text = "Please input your old password and what password you would like to change it to.\n Also input the file path of the file whose password is being changed", padx = 50, pady = 50, bg = "#f6f6f6", font=("Comic Sans", 14))
    titleLabel.grid(row = 1, column = 1, columnspan = 5)
    titleLabel.pack_propagate(0) # don't shrink

    FileLabel = Label(PassGUI, text = "File Path:", pady = 15, bg = "#f6f6f6")
    FileLabel.grid(row = 2, column = 1)
    FileLabel.pack_propagate(0) # don't shrink

    fileentry = Entry(PassGUI, width = 90, fg="Black")
    fileentry.grid(row = 2, column = 2, columnspan = 3)
    fileentry.pack_propagate(0) # don't shrink

    filebutton = Button(PassGUI, text = "...", command = GetFilePath, bg = "#f6f6f6")
    filebutton.grid(row = 2, column = 6)
    filebutton.pack_propagate(0) # don't shrink

    OldPassLabel = Label(PassGUI, text = "Old Password:", pady = 15, bg = "#f6f6f6")
    OldPassLabel.grid(row = 3, column = 1)
    OldPassLabel.pack_propagate(0) # don't shrink

    NewPassLabel = Label(PassGUI, text = "New Password:", pady = 15, bg = "#f6f6f6")
    NewPassLabel.grid(row = 4, column = 1)
    NewPassLabel.grid_propagate(0) # don't shrink

    RepeatLabel = Label(PassGUI, text = "Re-Enter New Password:", pady = 15, bg = "#f6f6f6")
    RepeatLabel.grid(row = 5, column = 1)
    RepeatLabel.grid_propagate(0) # don't shrink

    entry1 = Entry(PassGUI, width = 90, fg="Black", show = "*")
    entry1.grid(row = 3, column = 2, columnspan = 3)
    entry1.pack_propagate(0) # don't shrink

    entry2 = Entry(PassGUI, width = 90, fg="Black", show = "*")
    entry2.grid(row = 4, column = 2, columnspan = 3)
    entry2.pack_propagate(0) # don't shrink

    entry3 = Entry(PassGUI, width = 90, fg="Black", show = "*")
    entry3.grid(row = 5, column = 2, columnspan = 3)
    entry3.pack_propagate(0) # don't shrink

    ErrorLabel = Label(PassGUI, text = " ", pady = 30, bg = "#f6f6f6")
    ErrorLabel.grid(row = 6, column = 1, columnspan = 5)
    ErrorLabel.pack_propagate(0) # don't shrink

    button1 = Button(PassGUI, text = "Back", command = lambda: PassClick("Back"), padx = 15, pady = 15, bg = "#f6f6f6")
    button1.grid(row = 7, column = 1)
    button1.pack_propagate(0)

    button2 = Button(PassGUI, text = "Change Password", command = lambda: PassClick("Replace"), padx = 15, pady = 15, bg ="#f6f6f6")
    button2.grid(row = 7, column = 4, columnspan = 2)

    PassGUI.mainloop()

def NewKeyGUISetup():

    global KeyGUI, Combo, label2, nameentry

    KeyGUI = Tk()
    KeyGUI.title("Computer Car Keys: New Key")
    KeyGUI.geometry("1000x600+50+50")
    KeyGUI.configure(bg = "#f6f6f6")
    if (getPlatform() == "win"):
        KeyGUI.iconbitmap(r'CarKeyIcon.ico')

    # Variables 

    templist = rtrvDriveInfo(getPlatform())
    vlist = []

    for info in templist:
        if (info.getDrive() == "C:"):
            pass
        else:  
            vlist.append(info.getDrive())
            #vlist.append(info)
    
    if (vlist == []):
        vlist = ["No Valid Drives Found"]

    # Adding All Fill Layers

    labelfill1 = Label(KeyGUI, text = " ", pady = 50, bg = "#f6f6f6")
    labelfill1.grid(row = 0, column = 1, columnspan = 6)
    labelfill1.pack_propagate(0) # don't shrink

    labelfill2 = Label(KeyGUI, text = " ", padx = 50, bg = "#f6f6f6")
    labelfill2.grid(row = 0, column = 0, rowspan = 7)
    labelfill2.pack_propagate(0) # don't shrink

    # Adding All Production Layers

    label1 = Label(KeyGUI, text = "Select New Key to Reformat and Setup", padx = 200, pady = 50, bg = "#f6f6f6", font=("Comic Sans", 14))
    label1.grid(row = 1, column = 1, columnspan = 5)
    label1.pack_propagate(0) # don't shrink

    Combo = ttk.Combobox(KeyGUI, state = "readonly", values = vlist, width = 50)
    Combo.set("Pick an Option")
    Combo.grid(row = 3, column = 2, columnspan = 3)

    label2 = Label(KeyGUI, text = " ", bg = "#f6f6f6")
    label2.grid(row = 4, column = 2, columnspan = 3)
    label2.pack_propagate(0) # don't shrink

    label3 = Label(KeyGUI, text = "Drive Name:", bg = "#f6f6f6", pady = 50)
    label3.grid(row = 5, column = 1)
    label3.pack_propagate(0) # don't shrink

    nameentry = Entry(KeyGUI, width = 90, fg="Black")
    nameentry.grid(row = 5, column = 2, columnspan = 3)
    nameentry.pack_propagate(0) # don't shrink

    button1 = Button(KeyGUI, text = "Back", command = lambda: NewKeyClick("Back"), padx = 25, pady = 15, bg = "#f6f6f6")
    button1.grid(row = 6, column = 1)
    button1.pack_propagate(0)

    button2 = Button(KeyGUI, text = "Launch", command = lambda: NewKeyClick("Launch"), padx = 25, pady = 15, bg = "#f6f6f6")
    button2.grid(row = 6, column = 4, columnspan = 2)

##### Run the Program #####
MainGuiSetup()