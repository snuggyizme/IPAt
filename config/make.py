import FreeSimpleGUI as fsGUI
fsGUI.theme("LightGrey3")

from . import tools as configTools

def makeConfig(LANG_NAME: str, MAX_SOUND_LENGTH: str, SOUNDS: dict): # Compile the variables into the config format
    export = [f"{MAX_SOUND_LENGTH}|"]                                # SEE: config/tools.py
                                                                     # FOR FORMAT
    for character, ipa in SOUNDS.items():
        export.append(f"c{character},ipa{ipa}$")
    
    export.append(f"|{LANG_NAME}")

    return configTools.compileList(export)

def newConfig(): # Create new
    def createNewConfigLayout():
        return [[
            fsGUI.Text("Create New Language"),],
            [fsGUI.Text("Language Name:"), fsGUI.Push(), fsGUI.InputText(key="-LANG_NAME-")],
            [fsGUI.Text("Longest Graph:"), fsGUI.Push(), fsGUI.InputText(key="-MAX_SOUND_LENGTH-")],
            [fsGUI.Button("<- Back"), fsGUI.Button("Save and Continue")]
        ]
    
    def createAddSoundsLayout():
        return [[
            fsGUI.Text(f"Add sounds to {langName}:")],
            [fsGUI.Text("Character(s) (Uppercase):"), fsGUI.Push(), fsGUI.InputText(key="-CHAR_CAP-")],
            [fsGUI.Text("Character(s) (Lowercase):"), fsGUI.Push(), fsGUI.InputText(key="-CHAR_LOWER-")],
            [fsGUI.Text("IPA Symbol(s):"), fsGUI.Push(), fsGUI.InputText(key="-IPA_SYMBOL-")],
            [fsGUI.Button("Add Sound"), fsGUI.Button("Finish")]
        ]

    # ----   Create New Config Window   ----
    window = fsGUI.Window("IPAt - Create New Language", createNewConfigLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
    while True:
        event, values = window.read()
        if event == fsGUI.WIN_CLOSED or event == "<- Back":
            window.close()
            break
        if event == "Save and Continue":
            langName: str = values["-LANG_NAME-"]
            maxSoundLength: int = int(values["-MAX_SOUND_LENGTH-"])
            soundsWindow = fsGUI.Window(f"IPAt - Add Sounds to {langName}", createAddSoundsLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
            window.close()
            break
    # ---- END Create New Config Window ----
    
    # ----   Add Sounds Window   ----
    sounds: dict = {}
    addingSounds: bool = True
    while addingSounds:
        event, values = soundsWindow.read()

        if event == "Add Sound":
            charCap: str = values["-CHAR_CAP-"]
            charLower: str = values["-CHAR_LOWER-"]
            ipaSymbol: str = values["-IPA_SYMBOL-"]
            sounds[charCap + charLower] = ipaSymbol

            soundsWindow["-CHAR_CAP-"].update("")
            soundsWindow["-CHAR_LOWER-"].update("")
            soundsWindow["-IPA_SYMBOL-"].update("")
        
        if event == "Finish":
            addingSounds = False
            soundsWindow.close()
            break
    # ---- END Add Sounds Window ----
    
    fsGUI.popup("Config created successfully!", no_titlebar=True, keep_on_top=True, grab_anywhere=True)
    return makeConfig(langName, maxSoundLength, sounds)
    
