import FreeSimpleGUI as fsGUI
fsGUI.theme("LightGrey1")

def makeConfig(LANG_NAME: str, MAX_SOUND_LENGTH: str, SOUNDS: dict): # Compile the variables into the config format
    pass

def newConfig(): # Create new
    def createNewConfigLayout():
        return [[
            fsGUI.Text("Create New Language"),
            fsGUI.Button("Save and Continue")],
            [fsGUI.InputText("Language Name:", key="-LANG_NAME-")],
            [fsGUI.InputText("Longest Graph:", key="-MAX_SOUND_LENGTH-")],
            [fsGUI.Button("<- Back")]
        ]
    
    def createAddSoundsLayout():
        return [[
            fsGUI.Text(f"Add sounds to {langName}:")]
            [fsGUI.InputText("Character(s) (Uppercase):", key="-CHAR_CAP-")],
            [fsGUI.InputText("Character(s) (Lowercase):", key="-CHAR_LOWER-")],
            [fsGUI.InputText("IPA Symbol(s):", key="-IPA_SYMBOL-")],
            [fsGUI.Button("Add Sound"), fsGUI.Button("Finish")]
        ]

    window = fsGUI.Window("IPAt - Create New Language", createNewConfigLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
    while True:
        event, values = window.read()
        if event == fsGUI.WIN_CLOSED or event == "<- Back":
            window.close()
            break
        if event == "Save and Continue":
            langName: str = values["-LANG_NAME-"]
            maxSoundLength: str = values["-MAX_SOUND_LENGTH-"]
            soundsWindow = fsGUI.Window(f"IPAt - Add Sounds to {langName}", createAddSoundsLayout(), no_titlebar=True, grab_anywhere=True, keep_on_top=True)
            window.close()
            break
    
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
    
    makeConfig(langName, maxSoundLength, sounds)

    # print("Create New Language")
    # print("-------------------")

    # print("Language Name:")
    # LANG_NAME = input("> ")
    
    # print("Longest graph:")
    # MAX_SOUND_LENGTH = input("> ")

    # done = False
    # SOUNDS = {}
    # while not done:
    #     sound: list = []
    #     print("                         Type STOP to stop adding sounds.")
    #     print("Start of char/ipa pair.  Type the character(s), beginning with a capital:")
    #     soundOrSTOP = input("> ")
    #     if soundOrSTOP == "STOP":
    #         done == True
    #     sound.append(soundOrSTOP)

    #     print("                         Type the character(s) in lowercase:")
    #     sound.append(input("> "))

    #     print("                         Type the IPA symbol(s):")
    #     sound.append(input("> "))

    #     SOUNDS[sound[0] + sound[1]] = sound[2]
    
    # makeConfig(LANG_NAME, MAX_SOUND_LENGTH, SOUNDS)

