import time
from turtle import textinput
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import askokcancel, showinfo, WARNING
import tkinter as tk
import linecache
import re
import ctypes
import shlex, subprocess
import base64


root = tk.Tk()
root.withdraw()
root.attributes('-topmost', True)
root.title('AL File Rename')

root.geometry('330x80+320+100')
open_file = filedialog.askdirectory()


line_number = "Phrase not found"
line=''
objectType=['CODEUNIT','PAGE','TABLE','REPORT','XMLPORT','QUERY','ENUM','INTERFACE']
extendsObjectType=['PAGEEXTENSION','TABLEEXTENSION']
allObjectTypes=['CODEUNIT','CODEUNITS','PAGES','TABLES','REPORTS','PAGE','TABLE','REPORT','XMLPORT','QUERY','ENUM','INTERFACE','PAGEEXTENSION','TABLEEXTENSION',]
objectTypes=[extendsObjectType,objectType]

particular_line=''
isExtendedType=False

if open_file != '':
    dir_list = os.listdir(open_file)
else:
    # messagebox.showinfo('WARNING!!','Please select the folder to rename the files and try again')
    os._exit(0)

fileNames_list=''

def cancel():
    os._exit(0)

def start():
    dir_listNew=[]

    for cc in dir_list:
        if not cc.endswith('.al'):
            # print(len(cc))
            kkr = ''.join(char for char in cc if char.isalnum())
            # print(len(kkr))
            capi = cc.upper()
            if capi !='LAYOUTS' and capi !='LAYOUT':
                if cc == kkr:
                    dir_listNew.append(cc)

    # print(dir_list)
    # print(dir_listNew)

    if not cc.endswith('.al'):
        dir_list.clear()
        for csk in dir_listNew:
            dir_list.append(csk)

    # print(dir_list)
    # print(dir_listNew)

    GB = len(dir_list)
    download = 0
    speed = 1
    kkd = True
    isRepeat = True
    while (download < GB):
        # isFolder = False
        for folderName in dir_list:
            time.sleep(0.05)
            bar['value'] += (speed / GB) * 100
            download += speed
            percent.set(str(int((download / GB) * 100)) + "%")
            text.set(str(download) + "/" + str(GB) + " GB completed")
            window.update_idletasks()
            window.update()

            if kkd and isRepeat:
                if folderName.endswith('.al'):
                    fileNames_list = dir_list
                    isFolder=False
                    isRepeat = False
                    kkd = False
                else:
                    fileNames_list = os.listdir(open_file+'//'+folderName)
                    isFolder=True
                    isRepeat = True
                    kkd = True
                for oldName in fileNames_list:
                    extendedObjectTypeName = ''
                    if isFolder:
                        os.chdir(open_file + '/' + folderName)
                    else:
                        os.chdir(open_file)
                    for objectTypesName in objectTypes:

                        for objectTypesValue in objectTypesName:

                            if extendedObjectTypeName =='':
                                if isFolder:
                                    a_file = open(open_file + '/' + folderName + '/' + oldName, "r")
                                else:
                                    a_file = open(open_file + '/' + oldName, "r")
                                for number, line in enumerate(a_file):
                                    line_number = number + 1
                                    line = line.upper()
                                    position=0;
                                    if re.search(r"\b" + re.escape(objectTypesValue) + r"\b", line) and line_number<=4:
                                        position=line.find(objectTypesValue)
                                        check_spl_Char = line[0:position]
                                        rem_char_after_spl_char_remove = ''.join(char for char in check_spl_Char if char.isalnum())
                                        if position==0 or len(rem_char_after_spl_char_remove) == 0:
                                            if extendsObjectType.__contains__(objectTypesValue):
                                                isExtendedType = True
                                            else:
                                                isExtendedType = False

                                            line_number = number + 1
                                            line = line
                                            extendedObjectTypeName = objectTypesValue

                                            if isFolder:
                                                particular_line = linecache.getline(open_file + '/' + folderName + '/' + oldName, line_number)
                                            else:
                                                particular_line = linecache.getline(open_file + '/' + oldName, line_number)
                                            break

                    a_file.close()
                    line=[]
                    if isExtendedType:
                        line = particular_line.split('EXTENDS')
                    elif extendedObjectTypeName !='':
                        line = particular_line.split(extendedObjectTypeName)


                    if len(line) >=1:
                        originalLine = line
                        line = line[0].split()

                        i = 0
                        startLine = 0
                        endLine = 0
                        objectName = ''
                        objectNameExtensionWithQuotes=''

                        for mnc in line:
                            if line[i][0] == '"':
                                startLine = i
                            if line[i].endswith('"'):
                                endLine = i
                                break
                            i = i + 1

                        if isExtendedType:
                            for mnc in line:
                                if line[2][0] !='"':
                                    startLine = line[2]
                                    objectNameExtensionWithQuotes = line[2]


                        if startLine == 0:
                            objectName = line[2]
                        else:
                            originalLine = originalLine[0].split('"')
                            objectName = originalLine[1].replace(" ", "")
                            objectName = ''.join(char for char in objectName if char.isalnum())
                            if objectNameExtensionWithQuotes !='':
                                objectName = ''.join(char for char in objectNameExtensionWithQuotes if char.isalnum())
                        if extendedObjectTypeName.upper() == "PAGEEXTENSION":
                            extendedObjectTypeName = 'Page_Ext'
                        if extendedObjectTypeName.upper() == "TABLEEXTENSION":
                            extendedObjectTypeName = 'Table_Ext'
                        if extendedObjectTypeName.upper() == "REPORTEXTENSION":
                            extendedObjectTypeName = 'Report_Ext'
                        extendedObjectTypeName = extendedObjectTypeName.capitalize().replace('_ext', 'Ext')

                        gitRename = "git mv *#$.\\" + oldName + "*#$ .\\" + objectName + "." + extendedObjectTypeName + ".al"
                        gitRename = gitRename.replace('*#$','"')
                        if oldName!=objectName + "." + extendedObjectTypeName + ".al" :
                            if isFolder:
                                gitStatus= "git status *#$"+open_file+"/"+folderName+"/"+oldName+'"'
                                gitStatus = gitStatus.replace('*#$', '"')
                                # print(gitStatus)
                                output = subprocess.check_output(gitStatus,
                                                        shell=True)

                            else:
                                gitStatus = "git status *#$" + open_file + "/" + oldName + '"'
                                gitStatus = gitStatus.replace('*#$', '"')
                                # print(gitStatus)
                                output = subprocess.check_output(gitStatus,
                                    shell=True)

                            if str(output).__contains__('Untracked files'):
                                # rename = ".\\" + oldName + ", " + ".\\" + objectName + "." + extendedObjectTypeName+ ".al"
                                src = ".\\" + oldName
                                # src = src.replace('*#$', "'")
                                # src = '"'+src+'"'
                                desc = ".\\" + objectName + "." + extendedObjectTypeName + ".al"
                                # print(src)
                                # print(desc)
                                os.rename(src, desc)
                            else:
                                si = subprocess.STARTUPINFO()
                                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                                # si.wShowWindow = subprocess.SW_HIDE # default
                                subprocess.call(gitRename, startupinfo=si)
                                # gitRenameValue = os.system(gitRename)

        # print(download, '---', GB)
        if (download == GB):
            ctypes.windll.user32.MessageBoxW(0, "All Files have been successfully renamed in GIT using 'git mv'. \nCheck the Staged changes to see the renamed files. \nThank you for using RebelSkool's AL File Rename App.", "Info")
            dir_list.clear()
            window.update()
            os._exit(0)



# LOADING - START
window = Tk()
window.title('AL File Rename')
window.geometry('350x100+600+370')
# window.geometry('400x250+1000+300')

percent = StringVar()
text = StringVar()

bar = Progressbar(window,orient=HORIZONTAL,length=280)
bar.pack(pady=8)

# percentLabel = Label(window,textvariable=percent).pack(pady=10)
# taskLabel = Label(window,textvariable=text).pack(pady=10)
validFolders=[]
validFolderPresent=False
for cc in dir_list:
    if not cc.endswith('.al'):
        # print(len(cc))
        kkr = ''.join(char for char in cc if char.isalnum())
        # print(len(kkr))
        capi = cc.upper()
        if capi != 'LAYOUTS' and capi != 'LAYOUT':
            if cc == kkr:
                validFolders.append(cc)
    else:
        validFolderPresent=True

if not validFolderPresent:
    for mnm in allObjectTypes:
        mnm = mnm.upper()
        for valid in validFolders:
            valid = valid.upper()
            if valid == mnm:
                validFolderPresent=True


isFolder=True
isRepeat = True
button = Button(window,text="Rename Files in GIT",command=start).pack()
button = Button(window,text="Cancel",command=cancel).pack(pady=2)

print(str(button))

def disable_event():
   pass

window.protocol("WM_DELETE_WINDOW", disable_event)
if validFolderPresent:
    window.wm_attributes('-toolwindow', 'True')
    window.mainloop()
else:
    ctypes.windll.user32.MessageBoxW(0, "No AL Files found for renaming. Please choose the Source folder containing the AL files!","Info")
# LOADING - END

# ctypes.windll.user32.MessageBoxW(0, "File Renaming is Successfully Completed By RebelSkool App","HOORAY!!!")




