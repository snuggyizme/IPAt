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

LANGS: dict = data.langs
FINISHED_WORDS: list = []
PLAYLIST: list = []
SELECTED_LANGUAGE = None

# VERSION
# ----------------------------------------------
VERSION = 0.36

def startUp():
    appData = data.loadData(file="appdata")

    if appData["version"] == 0:
        appData["lastLanguage"] = "English"

    appData["version"] = VERSION
    data.saveData(appData, file="appdata")

    SELECTED_LANGUAGE = appData["lastLanguage"]

# ----------------------------------------------

# LAYOUTS
# ----------------------------------------------

def createHomeLayout():                             # Home 
    return [[fsGUI.Text("IPAt", font=("Arial", 60)), fsGUI.Push(), fsGUI.Text(data.loadData(file="appdata")["version"])],
            [fsGUI.Button("Import/Create a language config"),
             fsGUI.Button("Create IPA for words"),
             fsGUI.Button("Close")]]

def createIoCLayout():                              # Import or Create
    return [[fsGUI.Button("Import (Paste from clipboard)")],
            [fsGUI.Button("Make new")],
            [fsGUI.Button("<- Back")]]

def createSLoCWLayout():                            # Select Languae or Create Words
    return [[fsGUI.Text("Select Language or Create Words")],
            [fsGUI.Button("Select Language"), fsGUI.Button("Create Words")],
            [fsGUI.Button("<- Back")]]

def createSelectLangLayout():                       # Select / Inspect / Delete Language
    langButtons = []
    for lang in LANGS.values():
        langButtons.append([
            fsGUI.Text(configTools.extractLanguage(lang)["LANG_NAME"]),
            fsGUI.Push(),
            fsGUI.Button("Select", key=f"select_{configTools.extractLanguage(lang)['LANG_NAME']}"),
            fsGUI.Button("Inspect", key=f"inspect_{configTools.extractLanguage(lang)['LANG_NAME']}"),
            fsGUI.Button("Delete", key=f"delete_{configTools.extractLanguage(lang)['LANG_NAME']}")])

    return [[fsGUI.Text("Select Language")]] + langButtons + [[fsGUI.Button("<- Back")]]

def createWordScrollerLayout(mgl: int):             # Word Scroller
    export = [[
        fsGUI.Text(key="-LEFT-"), fsGUI.Push(),
        fsGUI.Text(key="-CURRENT-"), fsGUI.Push(),
        fsGUI.Text(key="-RIGHT-"),
    ],
    [], # Placeholder for graphs
    [fsGUI.Button("Add words to playlist"), fsGUI.Button("<- Back")]]

    for i in range(mgl):
        export[1].append(fsGUI.Text(key=f"-GRAPH_{i}-"))

    return export

def createPastePlaylistLayout():                    # Paste Playlist
    return [[fsGUI.Text("Paste words to be added to the playlist, seperated by newlines:")],
            [fsGUI.Multiline(size=(40, 10), key="-PLAYLIST_INPUT-")],
            [fsGUI.Button("Add to Playlist"), fsGUI.Push(), fsGUI.Button("<- Back")]]
# ----------------------------------------------

# MAIN APP
# ----------------------------------------------

def wordScroller(maxGraphLength: int):
    mainWindow = fsGUI.Window("IPAt", createWordScrollerLayout(maxGraphLength), no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    # ----   Main App Window   ----
    while True:
        event, values = mainWindow.read()

        if event == fsGUI.WIN_CLOSED or event == "<- Back":
            mainWindow.close()
            break

        if event == "Add words to playlist":
            clplWindow = fsGUI.Window("IPAt", createPastePlaylistLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
            
            # ----   Paste Playlist   ----
            while True:
                clplEvent, clplValues = clplWindow.read()

                if clplEvent == fsGUI.WIN_CLOSED or clplEvent == "<- Back":
                    clplWindow.close()
                    break

                if clplEvent == "Add to Playlist":
                    PLAYLIST.extend(clplValues["-PLAYLIST_INPUT-"].split("\n"))
                    clplWindow.close()
                    break
            # ---- END Paste Playlist ----

        word = PLAYLIST[0]
        FINISHED_WORDS.append("")
        for i in range(len(word)):
            while True:
                left = word[0:i]
                current = word[i]
                right = word[i+1:]

                mainWindow["-LEFT-"].update(left)
                mainWindow["-CURRENT-"].update(current)
                mainWindow["-RIGHT-"].update(right)

                POSSIBLE_GRAPHS: dict = {}
                LONGEST_POSSIBLE_GRAPH = 0

                for j in SELECTED_LANGUAGE["SOUNDS"].keys():
                    jUPPER = j[len(j)//2:len(j)]
                    jLOWER = j[0:len(j)//2]

                    if i == 0:
                        casedJ = jUPPER
                    else:
                        casedJ = jLOWER

                    if word[i:i+len(casedJ)] == casedJ:
                        POSSIBLE_GRAPHS[len(casedJ)].append(casedJ)

                        if len(casedJ) > LONGEST_POSSIBLE_GRAPH:
                            LONGEST_POSSIBLE_GRAPH = len(casedJ)

                for k in range(maxGraphLength):
                    if k in POSSIBLE_GRAPHS:
                        mainWindow[f"-GRAPH_{k}-"].update(disabled=False)
                    if k > LONGEST_POSSIBLE_GRAPH:
                        mainWindow[f"-GRAPH_{k}-"].update(disabled=True)

                if event.startswith("-GRAPH_"):
                    graphLength = int(event[len("-GRAPH_")])
                    selectedGraph = word[i:i+graphLength]
                    PLAYLIST[-0] += SELECTED_LANGUAGE["SOUNDS"][selectedGraph]
                    

                
                
    
    # ---- END Main App Window ----

    
        
    
    return FINISHED_WORDS

# ----------------------------------------------

def main():
    startUp()

    if not "English" in LANGS:
        LANGS["English"] = configTools.defaultCompiled
        data.saveData(LANGS)

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
                        LANGS[extractedConfig["LANG_NAME"]] = extractedConfig
                        data.saveData(LANGS)
                        print(f"New language imported from clipboard: {extractedConfig["LANG_NAME"]}")
                    except Exception as x:
                        fsGUI.popup(f"Error importing config from clipboard", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                
                
                if IoCevent == "Make new":
                    newConfig = configTools.extractLanguage(makeConfig.newConfig())
                    if newConfig:
                        try:
                            LANGS[newConfig["LANG_NAME"]] = makeConfig.makeConfig(newConfig["LANG_NAME"], newConfig["MAX_SOUND_LENGTH"], newConfig["SOUNDS"])
                            data.saveData(LANGS)

                            print(f"New language created: {newConfig['LANG_NAME']}")
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
                    slWindow = fsGUI.Window("IPAt - Select Language", createSelectLangLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)

                    # ----   Select Language   ----
                    while True:
                        event, values = slWindow.read()
                        if event == fsGUI.WIN_CLOSED or event == "<- Back": # I keep adding this redundant check, but whatever, copy paste go brrr
                            slWindow.close()
                            break
                        
                        if event.startswith("select_"):
                            langName = event[len("select_"):]
                            fsGUI.popup(f"Language '{langName}' selected!", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                            SELECTED_LANGUAGE = LANGS[langName]
                            slWindow.close()
                            break

                        if event.startswith("inspect_"):
                            langName = event[len("inspect_"):]
                            langData = LANGS[langName]

                            fsGUI.Print(langData, no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                            slWindow.close()
                            break

                        if event.startswith("delete_"):
                            langName = event[len("delete_"):]
                            confirm = fsGUI.popup_yes_no(f"Are you sure you want to delete the language '{langName}'?", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                            if confirm == "Yes":
                                del LANGS[langName]
                                data.saveData(LANGS)
                                fsGUI.popup(f"Language '{langName}' deleted!", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                                slWindow.close()
                                break
                    # ---- END Select Language ----
                
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
