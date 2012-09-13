#!/usr/bin/env python3

import sys
import os

KORPUS     = "/info/adk12/labb1/korpus"
STRIPPER   = "\"\n\t!%&'()*+,-./0123456789:;=?_€§¤©®·°[]$<>@´`"
KONKORDANS = "index.txt"

def find_word(word, konkordans):
    word = word.lower()
    hash = lazy_hash(word, 3)
    print("Hashade '"+word+"' som "+str(hash)+".")
    number_found = []
    with open(konkordans) as f:
        for line in f:
            if word in line.lower():
                number_found.append( line.split()[0] )
    print("Hittade %d matchande termer:" % len(number_found))
    result = ", ".join(number_found)
    return result


## Potential bug! The hashing doesn't account for special characters
## such as ':/.-' in the middle of the word. As of now, we just ignore
## these.
def lazy_hash(word, length):
    hash = 0
    for i, character in enumerate(word[0:length]):
        val = ord(character) - 96 # ord('a') = 97
        if val < 0: continue
        elif val > 26:
            # if character == 'å': val = 27
            # else if character == 'ä': val = 28
            # else if character == 'ö': val = 29
            if   val == 133: val = 27
            elif val == 132: val = 28
            elif val == 150: val = 29
            else: continue
        hash += val*30**i
    return hash

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
                    i += len(word)
            i += len(line)

    with open(filename, encoding="UTF-8", mode="wt") as f:
        for word in sorted(words):
            #f.write(str(lazy_hash(k,3)) + " " + str(k[4:]))
            f.write(word + "\n")
            #f.write(str(len(t[1])) + " " + t[0] + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-b":
            create_konkordans(KONKORDANS)
        else:
            result = find_word(sys.argv[1], KONKORDANS)
            print(result)
    else:
        # Behöver vi skapa konkordansen?
        if not os.path.isfile(KONKORDANS):
            create_konkordans(KONKORDANS)

