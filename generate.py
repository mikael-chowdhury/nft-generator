from PIL import Image
import random
import json
import sys
import os

import config as conf
import rconfig as rconf

nftNumber = 1

generated = []

loadedAssets = []

for item in os.listdir("./assets"):
    l = Image.open(f"./assets/{item}").convert("RGBA")
    l.load()
    l.convert("RGBA")
    loadedAssets.append({ "name": item.replace(".png", ""), "image": l })

sys.setrecursionlimit(2147483647)

def getImageByName(assetName):
    asset = None

    for item in loadedAssets:
        if item["name"] == assetName:
            asset = item

    return asset["image"]

def generateNFT():
    global nftNumber

    def getAssets():
        chosen = []
        chosenAssets = []

        for layer in conf.layers:
            chance = rconf.layers[layer]
            rand = random.randrange(0, 100000)

            if chance * 1000 >= rand:
                chosen.append(layer)

        for layer in chosen:
            rarity = rconf.tickets[layer]

            raritylist = []

            count = 0
            for item in rarity.keys():
                count += rarity[item]
                for i in range(int(rarity[item] * 100)):
                    raritylist.append(f"{conf.assetLocation}/{layer}_{item}.png")
            
            for i in range(int(100 - count) * 100):
                raritylist.append(f"{layer}_None")

            rand = random.randrange(0, 10000)

            chosenAssets.append(raritylist[rand])

        if not chosenAssets in generated:
            return chosenAssets
        else:
            del raritylist
            del chosen
            del chosenAssets
            return getAssets()

    chosenAssets = getAssets()

    final = Image.open(chosenAssets[0]).convert("RGBA")

    final.load()

    for i in range(len(chosenAssets)):
        if not "None" in chosenAssets[i]:
            name = chosenAssets[i].split("/")
            name = name[len(name) - 1].replace(".png", "")
            l = getImageByName(name)

            final.load()
            final.convert("RGBA")

            final = Image.alpha_composite(final, l)

    final.save(f"{conf.buildDirectoryNFTS}/{conf.project_name}#{nftNumber}.png")

    final.thumbnail((500, 500), Image.ANTIALIAS)
    final.save(f"{conf.buildDirectoryLowerNFTS}/{conf.project_name}#{nftNumber}.png")

    final.close()

    metadata = {
        "attributes": []
    }

    index = 0
    for image in chosenAssets:
        data = image.split("/")

        name = data[len(data) - 1].replace(".png", "")
        type = name.split("_")[0]

        metadata[type] = name
        metadata["attributes"].append({
            "trait_type": type,
            "value": name
        })
            
        index += 1

    for layer in conf.layers:
        if not layer in metadata.keys():
            metadata[layer] = "None"
            metadata["attributes"].append({
                "trait_type": layer,
                "trait_value": "None"
            })
    
    metadata["id"] = nftNumber

    json_string = json.dumps(metadata)

    with open(f"{conf.buildDirectoryMETA}/{conf.project_name}#{nftNumber}.json", "w") as f:
        f.write(json_string)
        f.close()

    generated.append(chosenAssets)

    if nftNumber <= rconf.TARGET_AMOUNT:
        print(f"generated nft {nftNumber}/{rconf.TARGET_AMOUNT}")
        nftNumber += 1
    else:
        print(f"\n\nGENERATED {nftNumber} {conf.project_name} NFTS :D\n\n")

        for asset in loadedAssets:
            asset["image"].close()

        exit(0)

while nftNumber < rconf.TARGET_AMOUNT:
    generateNFT()