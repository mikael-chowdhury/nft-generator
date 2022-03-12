import os
import json

loc = 20

usedAssets = []

for metafile in os.listdir("./meta"):
    with open(f"./meta/{metafile}", "r") as f:
        raw = f.read(6400)
        _json = json.loads(raw)

        for asset in _json.values():
            if not asset in usedAssets :
                usedAssets.append(asset)

def hasAssetBeenUsed(assetName) -> bool:
    hasBeenUsed = assetName in usedAssets

    return hasBeenUsed

totalAssets = 0
totalAssetsUsed = 0

for asset in os.listdir("./assets"):
    assetName = asset.replace(".png", "")

    used = hasAssetBeenUsed(assetName)

    condition = "✔" if used else "❌"

    totalAssets += 1

    if used:
        totalAssetsUsed += 1

    print(assetName + (" " * (loc - len(assetName))) + condition)

print(f"\n\n{totalAssetsUsed}/{totalAssets} assets have been used")