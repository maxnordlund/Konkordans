#!/usr/bin/env python3

import sys, os
from Korpus import Korpus
from Index import Index

KORPUS_PATH = "/info/adk12/labb1/korpus"
INDEX_FILENAME = "index.dat"
ENCODING = "ISO-8859-1"

korpus = None

def print_results(indices, length, offset):
    print("Hittade %d resultat." % len(indices))
    if len(indices) < 25:
        length = 25
    elif length == None:
        choice = input("Hur många resultat vill du visa: ")
        if choice.isdigit():
            length = min(int(choice), len(indices))
        else:
            return
    
    for i in indices[:length]:
        line = korpus[offset:i:offset]
        line = line.decode(ENCODING).replace('\n',' ')
        print(line, end="\n")

def print_usage():
    print("konkordans.py av Dan och Max")
    print("Användning:")
    print('konkordans.py [-h | --help]      visa denna hjälptext')
    print('konkordans.py -b | --build       bygg nytt databasindex')
    print('konkordans.py [-n ANTAL] TERM    visa konkordans för söktermen.')
    print()
    print('Konkordansen visar 25 resultat om inte -n ANTAL sätts.')

def main(args):
    global korpus
    
    help_flags = ["-h", "--help"]
    build_flags = ["-b", "--build"]
    n_flag = ["-n"]
    
    def flag_set(flags):
        return any([flag in args for flag in flags])
    
    if len(args) == 1 or flag_set(help_flags):
        print_usage()
        return
        
    building = (flag_set(build_flags) or not os.path.isfile(INDEX_FILENAME))
    
    n = None
    word = args[-1]
    if flag_set(n_flag):
        param = args[args.index("-n") + 1]
        if not param.isdigit() or int(param) < 0:
            print("Fel parameter till -n: ", param)
            return
        else:
            n = int(param)
    
    with Korpus(KORPUS_PATH) as korpus:
        index = Index()
        if building:
            print("Bygger index.")
            index.build(korpus)
            print("Index färdigbyggt.")
            if word in build_flags:
                return
        try:
            indices = index[word]
        except Exception as e:
            print("\nFel användning: ", e)
            print_usage()
        else:
            offset = 30 + len(word)
            print_results(indices, n, offset)


if __name__ == "__main__":
    main(sys.argv)
