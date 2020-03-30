import json

with open("SaveData.json", "r") as r:
    dat = json.load(r)
    print(dat)

