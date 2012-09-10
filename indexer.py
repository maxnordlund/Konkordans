#!/usr/bin/env python3

from collections import OrderedDict
import sys
import os

KORPUS     = "/info/adk12/labb1/korpus"
STRIPPER   = "\"\n\t!%&'()*+,-./0123456789:;=?_€§¤©®·°[]$<>@´`"
KONKORDANS = "index.txt"

def create_konkordans(filename):
    words = {}
    
    with open(KORPUS, encoding="ISO-8859-1") as f:
        i = f.tell()
        for line in f:
            for word in line.split(" "):
                i += 1
                stripped = word.strip(STRIPPER).lower()
                if stripped != "":
                    if stripped not in words:
                        words[stripped] = [i]
                    else:
                        words[stripped].append(i)
                    #l = words.setdefault(stripped, list())
                    #l.append(i)
                    i += len(word)
            i += len(line)
    
    words = OrderedDict(sorted(words.items(), key=lambda t: t[0]))

    with open(filename, encoding="UTF-8", mode="wt") as f:
        for t in words.items():
            #f.write(t[0] + " " + str(t[1]) + "\n")
            f.write(str(len(t[1])) + " " + t[0] + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-b":
            create_konkordans(KONKORDANS)
    else:
        # Behöver vi skapa konkordansen?
        if not os.path.isfile(KONKORDANS):
            create_konkordans(KONKORDANS)

