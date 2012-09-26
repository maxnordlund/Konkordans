#!/usr/bin/env python3

import sys, os
from Korpus import Korpus
from Index import Index

KORPUS_PATH = "/info/adk12/labb1/korpus"
INDEX_FILENAME = "index.dat"

def search_index(korpus, index, word, max_results=25):
    if type(max_results) is not int or max_results < 1:
        e = Exception("Antal resultat måste vara mer än noll!")
        raise e
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

def print_usage():
    print("konkordans.py av Dan och Max")
    print("Användning:")
    print('konkordans.py [-h | --help]      visa denna hjälptext')
    print('konkordans.py -b | --build       bygg nytt databasindex')
    print('konkordans.py [-n ANTAL] TERM    visa konkordans för söktermen.')
    print()
    print('Konkordansen visar 25 resultat om inte -n ANTAL sätts.')

if __name__ == "__main__":
    help_flags = ["-h", "--help"]
    build_flags = ["-b", "--build"]
    number_of_results_flag = ["-n"]
    if len(sys.argv) == 1 or sys.argv[1] in help_flags:
        print_usage()
        print_usage()
    elif sys.argv[1] in build_flags:
        print("Bygger index på " + INDEX_FILENAME + "...")
        with Korpus(KORPUS_PATH) as korpus:
            with Index(korpus) as index:
                index.build()
        print("Index färdigbyggt.")
    elif sys.argv[1] in number_of_results_flag:
        try:
            n, word = sys.argv[2:]
            with Korpus(KORPUS_PATH) as korpus:
                with Index(korpus) as index:
                    if not os.path.isfile(INDEX_FILENAME):
                        print("Hittade inget index, bygger det nu.")
                        index.build()
                    search_index(korpus, index, word, int(n))
        except Exception as e:
            print("\nFel användning: ", e)
            print_usage()
    else: # search for the provided term
        with Korpus(KORPUS_PATH) as korpus:
            with Index(korpus) as index:
                if not os.path.isfile(INDEX_FILENAME):
                    print("Hittade inget index, bygger det nu.")
                    index.build()
                word = sys.argv[1]
                search_index(korpus, index, word)
