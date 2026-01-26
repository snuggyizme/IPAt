# CONFIG STRUCTURE
# "<MAX_SOUND_LENGTH: INT>|c<CHARACTER_UPPER><CHARACTER_LOWER>,ipa<IPA>|<LANG_NAME>"
#                          \_________________________________________/
#                          ↑
#                          Repeatable, seperate with "$"

default = [
    "4|",
    "cAa,ipaæ$cAa,ipaɑ$cAa,ipaeɪ$cAa,ipaə$",
    "cBb,ipab$",
    "cCc,ipak$cCc,ipas$",
    "cDd,ipad$",
    "cEe,ipaɛ$cEe,ipaiː$cEe,ipaə$",
    "cFf,ipaf$",
    "cGg,ipag$",
    "cHh,ipah$",
    "cIi,ipaɪ$cIi,ipaiː$",
    "cJj,ipadʒ$",
    "cKk,ipak$",
    "cLl,ipal$",
    "cMm,ipam$",
    "cNn,ipan$",
    "cOo,ipaɒ$cOo,ipaoʊ$cOo,ipaə$",
    "cPp,ipap$",
    "cRr,ipaɹ$",
    "cSs,ipas$",
    "cTt,ipat$",
    "cUu,ipaʌ$cUu,ipajuː$cUu,ipaə$",
    "cVv,ipav$",
    "cWw,ipaw$",
    "cYy,ipaj$",
    "cZz,ipaz$",
    "cThth,ipaθ$cThth,ipað$",
    "cShsh,ipaʃ$",
    "cChch,ipatʃ$",
    "cNgng,ipaŋ",
    "|English"
]

def compileDefault(input: list):
    export: str = ""
    for i in input:
        export += i
    defaultCompiled = export
    return export

defaultCompiled: str = compileDefault(default)

def extractLanguage(input: str):
    export: dict = {"SOUNDS": {}}

    sections = input.split("|")

    export["MAX_SOUND_LENGTH"] = sections[0]
    export["LANG_NAME"] = sections[2]

    sounds: list = sections[1].split("$")
    for sound in sounds:
        splitSound: str = sound.split(",")
        character: str = splitSound[0][1:]
        ipa: str = splitSound[1][3:]

        export["SOUNDS"][character] = ipa

    return export


class Language:
    def __init__(self, config):
        language = extractLanguage(config)
        
        self.name = language["LANG_NAME"]
        self.maxSoundLength = language["MAX_SOUND_LENGTH"]
        self.sounds = language["SOUNDS"]