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
    "thTh,ipaθ$",
    "thTh,ipað$",
    "shSh,ipaʃ$",
    "chCh,ipatʃ$",
    "ngNg,ipaŋ",
    "|English"
]

defaultCompiled: str

def compileDefault(input):
    export: str = ""
    for i in input:
        export += i
    defaultCompiled = export
    return export
