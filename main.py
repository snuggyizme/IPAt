from config import tools as configTools
from config import make as makeConfig

import dataAccess as data

import math

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
VERSION = 0.40

def startUp():
    global SELECTED_LANGUAGE

    appData = data.loadData(file="appdata")

    if appData["version"] == 0:
        appData["lastLanguage"] = "English"

    appData["version"] = VERSION
    data.saveData(appData, file="appdata")

    SELECTED_LANGUAGE = appData["lastLanguage"]

# ----------------------------------------------

# LAYOUTS
# ----------------------------------------------

def uiArray(top, bottom, content):                  # Helper function
    columns = math.ceil(len(content) / 3)
    export = []
    for i in range(columns):
        u = i * 3
        row = []
        for c in range(3):
            if u + c < len(content):
                row.append(content[u+c])
            else:
                row.append(fsGUI.Push())

        export.append(row)

    return top + export + bottom

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
    t = [[
        fsGUI.Text(key="-LEFT-"), fsGUI.Push(),
        fsGUI.Text(key="-CURRENT-"), fsGUI.Push(),
        fsGUI.Text(key="-RIGHT-"),
    ]]
    b = [[fsGUI.Button("Add words to playlist"), fsGUI.Button("<- Back")]]

    c = []
    for i in range(mgl):
        c.append(fsGUI.Button(f"{i+1}", key=f"-GRAPH_{i+1}-", disabled=True))

    return uiArray(t, b, c)

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
                                                                                    # Need to comment this out it's confusing:
                                                                                    # ----------------------------------------
        word = PLAYLIST[0]                                                          # Get first word
        FINISHED_WORDS.append("")                                                   # Prepare space
        for i in range(len(word)):                                                  # For every character in the word:
            while True:
                left = word[0:i]                                                    # Get characters to left of current character
                current = word[i]                                                   # Get current character
                right = word[i+1:]                                                  # Get characters to right of current character

                mainWindow["-LEFT-"].update(left)                                   # Update left characters
                mainWindow["-CURRENT-"].update(current)                             # Update current character
                mainWindow["-RIGHT-"].update(right)                                 # Update right characters

                POSSIBLE_GRAPHS: dict = {}                                          # Reset the dictionary of possible graphs to select (key = Upper + Lower, value = IPA)
                LONGEST_POSSIBLE_GRAPH = 0                                          # Reset the longest possible graph length. We need this to cut off all buttons that are too high.

                for j in SELECTED_LANGUAGE["SOUNDS"].keys():                        # For every sound in the selected language:
                    jUPPER = j[len(j)//2:len(j)]                                    # Get the upper case version of the graph
                    jLOWER = j[0:len(j)//2]                                         # Get the lower case version of the graph

                    if i == 0:                                                      # If we're at the start of the word, use the uppercase version of the grapheme
                        casedJ = jUPPER
                    else:                                                           # Otherwise, use the lowercase version of the grapheme
                        casedJ = jLOWER

                    if word[i:i+len(casedJ)] == casedJ:                             # If the word matches the current character and the following characters up to the length of the grapheme:
                        POSSIBLE_GRAPHS[len(casedJ)].append(casedJ)                 # Add the grapheme to the possible graphs dictionary

                        if len(casedJ) > LONGEST_POSSIBLE_GRAPH:                    # If this grapheme is longer than the current longest possible graph:
                            LONGEST_POSSIBLE_GRAPH = len(casedJ)                    # Update the longest possible graph length to be this grapheme's length

                for k in range(maxGraphLength):                                     # (Now out of the loop for every sound), for every grapheme length up to the max graph length:
                    if k in POSSIBLE_GRAPHS:                                        # If there are possible graphs of this length:
                        mainWindow[f"-GRAPH_{k}-"].update(disabled=False)           # Enable the button for this grapheme length
                    if k > LONGEST_POSSIBLE_GRAPH:                                  
                        mainWindow[f"-GRAPH_{k}-"].update(disabled=True)            # Otherwse, disable the button for this grapheme length

                if event.startswith("-GRAPH_"):                                     # (Now out of the loop for every grapheme length), if the event is one of the grapheme length buttons:
                    graphLength = int(event[len("-GRAPH_")])                        # Get the length of the grapheme from the button key
                    selectedGraph = word[i:i+graphLength]                           # Get the selected grapheme from the word
                    PLAYLIST[-0] += SELECTED_LANGUAGE["SOUNDS"][selectedGraph]      # Add the IPA for the selected grapheme to the finished words list
                    

                
                
    
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
                            global SELECTED_LANGUAGE

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
                    if not SELECTED_LANGUAGE:
                        fsGUI.popup("No language selected! Please select a language first.", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                        break
                    else:
                        wordScroller(int(SELECTED_LANGUAGE["MAX_SOUND_LENGTH"]))
                        SLoCWwindow.close()
                        window.close()

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
