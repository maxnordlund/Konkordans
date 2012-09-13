#!/usr/bin/env python3

import Links.Links as Links

class Index
    """En klass som pratar med indexfilen"""
    def __init__(self, korpus, index, lazy_hash, links, force=True):
        self._korpus = korpus
        self._index  = index
        self._hash   = lazy_hash
        self._links  = links
        
        i       = korpus.tell()
        words   = {}
        max_len = 0
        
        for line in korpus:
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
        
        self._links = Links()
        
        with open(filename, encoding="UTF-8", mode="wt") as f:
            for word in sorted(words):
                #f.write(str(lazy_hash(k,3)) + " " + str(k[4:]))
                f.write(word + "\n")
                #f.write(str(len(t[1])) + " " + t[0] + "\n")



