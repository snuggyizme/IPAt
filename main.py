from config import tools as configTools
from config import make as makeConfig

from pathlib import Path
import json

import pyperclip

import FreeSimpleGUI as fsGUI
fsGUI.theme("LightGrey1")

#__/\\\\\\\\\\\__/\\\\\\\\\\\\\_______/\\\\\\\\\__________________        
# _\/////\\\///__\/\\\/////////\\\___/\\\\\\\\\\\\\________________       
#  _____\/\\\_____\/\\\_______\/\\\__/\\\/////////\\\_____/\\\______      
#   _____\/\\\_____\/\\\\\\\\\\\\\/__\/\\\_______\/\\\__/\\\\\\\\\\\_     
#    _____\/\\\_____\/\\\/////////____\/\\\\\\\\\\\\\\\_\////\\\////__    
#     _____\/\\\_____\/\\\_____________\/\\\/////////\\\____\/\\\______   
#      _____\/\\\_____\/\\\_____________\/\\\_______\/\\\____\/\\\_/\\__  
#       __/\\\\\\\\\\\_\/\\\_____________\/\\\_______\/\\\____\//\\\\\___ 
#        _\///////////__\///______________\///________\///______\/////____

langs: list = []

def createHomeLayout():
    return [[fsGUI.Text("IPAt")],
            [fsGUI.Button("Import/Create a language config"),
             fsGUI.Button("Create IPA for words"),
             fsGUI.Button("Close")]]

def createIoCLayout():
    return [[fsGUI.Button("Import (Paste from clipboard)")],
            [fsGUI.Button("Import (Select File)")],
            [fsGUI.Button("Make new")],
            [fsGUI.Button("<- Back")]]

def main():
    window = fsGUI.Window("IPAt", createHomeLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    # ----   Home   ----
    while True:
        event, values = window.read()
        if event == fsGUI.WIN_CLOSED or event == "Close":
            window.close()
            break

        if event == "Import/Create a language config":
            IoCwindow = fsGUI.Window("IPAt", createIoCLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
            
            # ----   IoC   ----
            while True:
                IoCevent, IoCvalues = IoCwindow.read()

                if IoCevent == "Import (Paste from clipboard)":
                    clipboardData = pyperclip.paste()
                    try:
                        langs.append(configTools.extractLanguage(clipboardData))
                    except Exception as x:
                       fsGUI.popup(f"Error importing config from clipboard: {x}", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                

                if IoCevent == "Import (Select File)":
                    pass
                
                if IoCevent == "Make new":
                    makeConfig.newConfig()

                if IoCevent == fsGUI.WIN_CLOSED or IoCevent == "<- Back":
                    IoCwindow.close()
                    break
            # ---- END IoC ----
    # ---- END Home ----

def testLine():
    # print(configTools.compileList(configTools.default))           #  (Works)
    # print(configTools.extractLanguage(configTools.defaultCompiled))  #  (Works)
    pass

if __name__ == "__main__":
    main()
