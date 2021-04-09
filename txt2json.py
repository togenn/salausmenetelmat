import json

dict1 = {}

with open("sanalista_FI.txt") as txt:
    for rivi in txt:
        sana = rivi.strip().lower()

        dict1[sana] = 1

valmis_tiedosto = open("sanalista_FI.json", "w")
json.dump(dict1, valmis_tiedosto)
valmis_tiedosto.close()