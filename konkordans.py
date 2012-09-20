#!/usr/bin/env python3

import sys, os
from Korpus import Korpus
from Index import Index

KORPUS_PATH = "/info/adk12/labb1/korpus"

help_text = """Användning: 
"konkordans.py -h | --help" för att få denna hjälptext.
"konkordans.py -b | --build [filnamn]" för att bygga ett nytt databasindex och avsluta programmet. Byt filnamn till det du vill kalla indexet, eller kör utan för att låta det heta "index.dat".
"konkordans.pu <sökterm>" för att få en konkordans för söktermen."""

kommande_help_text = """Kör programmet utan argument för att starta en interaktiv session. Programmet kommer skapa """

INDEX_FILENAME = "index.dat"

def search(word):
    with Korpus(KORPUS_PATH) as korpus:
        with Index(korpus) as index:
            if not os.path.isfile(INDEX_FILENAME):
                print("Hittade inget index, bygger det nu.")
                index.build()

            limit = 10
            off = 30 + len(word)
            indices = index[word.strip().lower()]
            print("Antal resultat: ", len(indices))
            for i in indices[:limit]:
                line = korpus[off:i:off]
                line = line.decode("ISO-8859-1").replace('\n',' ')
                print(line, end="\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-b", "--build"]:
            print("Bygger index på " + INDEX_FILENAME + "...")
            with Korpus(KORPUS_PATH) as korpus:
                with Index(korpus) as index:
                    index.build()
            print("Index färdigbyggt.")
        elif sys.argv[1] in ["-h", "--help"]:
            print(help_text)
        else:
            search( sys.argv[1] )
    else:
        print("Den interaktiva session med sökning är inte färdig än.")

