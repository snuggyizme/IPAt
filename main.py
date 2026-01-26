from config import tools as configTools
from config import make as makeConfig

import pyperclip

import FreeSimpleGUI as fsGUI
fsGUI.theme("LightGrey1")

storedLanguages: list = []

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
                        storedLanguages.append(configTools.extractLanguage(clipboardData))
                    except Exception as x:
                       fsGUI.popup(f"Error importing config from clipboard: {x}", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                

                if IoCevent == "Import (Select File)":
                    pass
                
                if IoCevent == "Make new":
                    pass

                if IoCevent == fsGUI.WIN_CLOSED or IoCevent == "<- Back":
                    IoCwindow.close()
                    break
            # ---- END IoC ----
    # ---- END Home ----

def testLine():
    # print(configTools.compileDefault(configTools.default))           #  (Works)
    # print(configTools.extractLanguage(configTools.defaultCompiled))  #  (Works)
    pass

if __name__ == "__main__":
    main()
