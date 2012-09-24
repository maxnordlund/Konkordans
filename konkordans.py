#!/usr/bin/env python3

import sys, os
from Korpus import Korpus
from Index import Index

KORPUS_PATH = "/info/adk12/labb1/korpus"

USAGE = """Användning: 
"konkordans.py -h | --help" för att få denna hjälptext.
"konkordans.py -b | --build [filnamn]" för att bygga ett nytt databasindex och avsluta programmet. Byt filnamn till det du vill kalla indexet, eller kör utan för att låta det heta "index.dat".
"konkordans.py [-n <antal resultat=25>] <sökterm>" för att få en konkordans för söktermen."""

INDEX_FILENAME = "index.dat"

def search_index(korpus, index, word, max_results=25):
    try:
        off = 30 + len(word)
        indices = index[word.strip().lower()]
        print("Visar %d/%d resultat." % (max_results, len(indices)))
        for i in indices[:max_results]:
            line = korpus[off:i:off]
            line = line.decode("ISO-8859-1").replace('\n',' ')
            print(line, end="\n")
    except Exception as e:
        print("\nNågonting gick snett!")
        print(e)
    

def search(word, max_results):
    try:
        with Korpus(KORPUS_PATH) as korpus:
            with Index(korpus) as index:
                if not os.path.isfile(INDEX_FILENAME):
                    print("Hittade inget index, bygger det nu.")
                    index.build()

                off = 30 + len(word)
                indices = index[word.strip().lower()]
                print("Visar %d/%d resultat." % (max_results, len(indices)))
                for i in indices[:max_results]:
                    line = korpus[off:i:off]
                    line = line.decode("ISO-8859-1").replace('\n',' ')
                    print(line, end="\n")
    except Exception as e:
        print("\nNågonting gick snett!")
        print(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        term1 = sys.argv[1]
        if term1 in ["-b", "--build"]:
            print("Bygger index på " + INDEX_FILENAME + "...")
            with Korpus(KORPUS_PATH) as korpus:
                with Index(korpus) as index:
                    index.build()
            print("Index färdigbyggt.")
        elif term1 in ["-h", "--help"]:
            print(USAGE)
        elif term1 in ["-n"]:
            try:
                n, t = sys.argv[2:]
                search(str(t), int(n))
            except Exception as e:
                print("\nFel användning: ", e)
                print(USAGE)
        else:
            with Korpus(KORPUS_PATH) as korpus:
                with Index(korpus) as index:
                    if not os.path.isfile(INDEX_FILENAME):
                        print("Hittade inget index, bygger det nu.")
                        index.build()
                    search_index(korpus, index, word)
    else:
        print("Den interaktiva sessionen med sökning är inte färdig än.")
        print("Se användningsinstruktionerna:")
        print(USAGE)


