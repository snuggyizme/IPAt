from pathlib import Path
import json

from config import tools as configTools

dataFile = Path.home() / ".ipatlanguages.json"

def loadData():
    if not dataFile.exists():
        defaultData = {
            "English": configTools.defaultCompiled
        }
        saveData(defaultData)
        return defaultData
    with open(dataFile, "r", encoding="utf-8") as f:
        return json.load(f)

def saveData(data: dict):
    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
langs = loadData()
print(langs)