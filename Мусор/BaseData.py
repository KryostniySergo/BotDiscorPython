import json

Plat = {

}


def save():
    with open("SaveData.json", "w") as w:
        json.dump(Plat, w)

save()