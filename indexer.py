#!/usr/bin/env python3

import sys
import os

KORPUS = "/info/adk12/labb1/korpus"
KONKORDANS = "index.txt"

def create_konkordans(filename):
    words = set()
    
    with open(KORPUS, encoding="ISO-8859-1") as korpus:
        for line in korpus:
            for word in line.split():
                words.add(word.strip("!\"%&'()*+,-./0123456789:;=?_€§©®·[]$<>@`").lower())
        
        print("No. unique words: ", len(words))
        with open(filename, encoding="UTF-8", mode="wt") as index:
            for word in sorted(words):
                
                index.write(word + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-b":
            create_konkordans(KONKORDANS)
    else:
        # Behöver vi skapa konkordansen?
        if not os.path.isfile(KONKORDANS):
            create_konkordans(KONKORDANS)
