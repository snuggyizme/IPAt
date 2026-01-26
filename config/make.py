def makeConfig(LANG_NAME: str, MAX_SOUND_LENGTH: str, SOUNDS: dict): # Compile the variables into the config format
    pass

def importConfig(): # Paste from clipboard
    pass

def newConfig(): # Create new
    print("Create New Language")
    print("-------------------")

    print("Language Name:")
    LANG_NAME = input("> ")
    
    print("Longest graph:")
    MAX_SOUND_LENGTH = input("> ")

    done = False
    SOUNDS = {}
    while not done:
        sound: list = []
        print("                         Type STOP to stop adding sounds.")
        print("Start of char/ipa pair.  Type the character(s), beginning with a capital:")
        soundOrSTOP = input("> ")
        if soundOrSTOP == "STOP":
            done == True
        sound.append(soundOrSTOP)

        print("                         Type the character(s) in lowercase:")
        sound.append(input("> "))

        print("                         Type the IPA symbol(s):")
        sound.append(input("> "))

        SOUNDS[sound[0] + sound[1]] = sound[2]
    
    makeConfig(LANG_NAME, MAX_SOUND_LENGTH, SOUNDS)

