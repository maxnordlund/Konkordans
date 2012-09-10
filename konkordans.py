# coding=utf-8

import pickle
import sys
import os.path

KORPUS_PATH = "/info/adk12/labb1/korpus"
KONKORDANS_FILENAME = "index.dat"

# will return a hash based on the first three characters in the word
# all words should consist of alphabetic characters a-Ö
def lazy_hash(word):
    if len(word) < 3: 
        word += "   "
    
    index = 0
    mul = 0
    for character, m in zip(word[0:3].lower(), [1, 30, 900]):
        v = ord(character)-96 # ord("a") = 97
        if v < 0: v = 0 # " "
        if v == 132: v = 27 # "å"
        if v == 133: v = 28 # "ä"
        if v == 150: v = 29 # "ö"
        index += v * m 
    return index


# TODO skapa och spara pekare från hash till ordlista
# TODO spara index för varje ord
# TODO sortera indexen i första filen
# TODO skriv konkordansen till fil.
def create_konkordans(filename):
    strip_characters = "-'\"()$@*%></\\=[;&]_+!?:,.0123456789"
    words = set()
    i = 0
    with open(KORPUS_PATH, 'r', encoding="ISO-8859-1") as korpus:
        for line in korpus.readlines():
            for word in line.split():
                # save index of word
                words.add(word.strip(strip_characters))
                i += 1
                if not i % 1000:
                    print("Parsed {} words".format(i))
    hashes = dict()
    for word in words:
        hashes.setdefault(lazy_hash(word), list()).append(word) # should be an ordered set
    for i, k in zip(range(10), hashes.keys()): #deb
        print([k,hashes[k]])
    
    with open(filename, 'wb') as f:
        pickle.dump(hashes, f)

def parse_konkordans(filename):
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-b":
            create_konkordans(KONKORDANS_FILENAME)
    else:
        # Behöver vi skapa konkordansen?
        if not os.path.isfile(KONKORDANS_FILENAME):
            create_konkordans(KONKORDANS_FILENAME)



    


    
    
