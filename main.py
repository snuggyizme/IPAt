from config import tools as configTools
from config import make as makeConfig

import dataAccess as data

from pathlib import Path
import json

import pyperclip

import FreeSimpleGUI as fsGUI
fsGUI.theme("LightGrey3")

#__/\\\\\\\\\\\__/\\\\\\\\\\\\\_______/\\\\\\\\\__________________        
# _\/////\\\///__\/\\\/////////\\\___/\\\\\\\\\\\\\________________       
#  _____\/\\\_____\/\\\_______\/\\\__/\\\/////////\\\_____/\\\______      
#   _____\/\\\_____\/\\\\\\\\\\\\\/__\/\\\_______\/\\\__/\\\\\\\\\\\_     
#    _____\/\\\_____\/\\\/////////____\/\\\\\\\\\\\\\\\_\////\\\////__    
#     _____\/\\\_____\/\\\_____________\/\\\/////////\\\____\/\\\______   
#      _____\/\\\_____\/\\\_____________\/\\\_______\/\\\____\/\\\_/\\__  
#       __/\\\\\\\\\\\_\/\\\_____________\/\\\_______\/\\\____\//\\\\\___ 
#        _\///////////__\///______________\///________\///______\/////____

langs: dict = data.langs

def createHomeLayout():
    return [[fsGUI.Text("IPAt", font=("Arial", 60))], # Home
            [fsGUI.Button("Import/Create a language config"),
             fsGUI.Button("Create IPA for words"),
             fsGUI.Button("Close")]]

def createIoCLayout():            # Import or Create
    return [[fsGUI.Button("Import (Paste from clipboard)")],
            [fsGUI.Button("Make new")],
            [fsGUI.Button("<- Back")]]

def createSLoCWLayout():          # Select Languae or Create Words
    return [[fsGUI.Text("Select Language or Create Words")],
            [fsGUI.Button("Select Language"), fsGUI.Button("Create Words")],
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
                        extractedConfig = configTools.extractLanguage(clipboardData)
                        langs[extractedConfig["LANG_NAME"]] = extractedConfig
                        data.saveData(langs)
                        print(f"New language imported from clipboard: {extractedConfig["LANG_NAME"]}")
                    except Exception as x:
                        fsGUI.popup(f"Error importing config from clipboard", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                
                
                if IoCevent == "Make new":
                    newConfig = configTools.extractLanguage(makeConfig.newConfig())
                    if newConfig:
                        try:
                            langs[newConfig["LANG_NAME"]] = makeConfig.makeConfig(newConfig["LANG_NAME"], newConfig["MAX_SOUND_LENGTH"], newConfig["SOUNDS"])
                            data.saveData(langs)

                            print(f"New language created: {langs[-1]['LANG_NAME']}")
                        except Exception as x:
                            fsGUI.popup(f"Error creating new config", no_titlebar=True, keep_on_top=True, grab_anywhere=True)

                if IoCevent == fsGUI.WIN_CLOSED or IoCevent == "<- Back":
                    IoCwindow.close()
                    break
            # ---- END IoC ----

        if event == "Create IPA for words":
            SLoCWwindow = fsGUI.Window("IPAt", createSLoCWLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
            
            # ----   SLoCW   ----
            while True:
                SLoCWevent, SLoCWvalues = SLoCWwindow.read()

                if SLoCWevent == "Select Language":
                    def createSelectLangLayout():
                        langButtons = []
                        for lang in langs:
                            langButtons.append([fsGUI.Button(lang["LANG_NAME"])])
                        return [[fsGUI.Text("Select Language")]] + langButtons + [[fsGUI.Button("<- Back")]]

                if SLoCWevent == "Create Words":
                    pass

                if SLoCWevent == fsGUI.WIN_CLOSED or SLoCWevent == "<- Back":
                    SLoCWwindow.close()
                    break
            # ---- END SLoCW ----
    # ---- END Home ----

def testLine():
    # print(configTools.compileList(configTools.default))           #  (Works)
    # print(configTools.extractLanguage(configTools.defaultCompiled))  #  (Works)
    pass

if __name__ == "__main__":
    main()

