import os
import json

def getLoadedMeta():
    loaded = []

    for metafile in os.listdir("./meta"):
        with open(f"./meta/{metafile}", "r") as f:
            raw = f.read(6400)
            _json = json.loads(raw)
            loaded.append(_json)

    return loaded