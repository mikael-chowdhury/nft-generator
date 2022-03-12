#!/usr/bin/python

import sys
import metautils

args = sys.argv
del args[0]

keys = []
values = []

VIEW = False

index = 0
while index < len(args):
    if args[index].startswith("--"):
        keys.append(args[index].replace("--", ""))

        if not args[index].replace("--", "") == "view":
            values.append(args[index + 1])

        index += 1

    index += 1

if "view" in keys:
    i = keys.index("view")
    del keys[i]

    VIEW = True

found = []

loaded = metautils.getLoadedMeta()

for metafile in loaded:
    index = 0

    spec = True

    for key in keys:
        if not metafile[key] == values[index]:
            spec = False

        index += 1

    if spec == True:
        found.append(metafile)

if not VIEW:
    print("\n" + str(len(found)) + " nfts meet this specification, add the --view flag to see what ids meet this specification\n")
else:
    print("\n")
    if len(found) == 0:
        print("no nfts meet these specifications")
    else:
        for item in found:
            print(item["id"])

        print("\n" + str(len(found)) + " nfts meet this specification")