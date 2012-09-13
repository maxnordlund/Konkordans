#!/usr/bin/env python3

import sys
import os

if __name__ == "__main__":
    with Korpus(fil) as korpus:
        with Index(korpus) as i:
            if build:
                i.create()
            for i in Index[search][:limit]:
                korpus[off:i:off]

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

