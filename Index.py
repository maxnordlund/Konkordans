#!/usr/bin/env python3

import Links.Links as Links

class Index:
    """En klass som pratar med indexfilen"""
    def __init__(self, korpus, index_path="index.dat", link_path="links.dat"):
        self._korpus     = korpus
        self._index_path = index_path
        self._link_path  = link_path
        with open("hash.dat", mode="r+b") as h:
            self._hash   = Hash(h)
    
    def __enter__(self):
        self._fil   = open(self._index_path, mode="r+b", encoding=ISO).__enter__()
        self._links = open(self._link_path,  mode="r+b")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._fil.__exit__(exc_type, exc_val, exc_tb)
    
    def create(self):
        index   = self._korpus.tell()
        words   = {}
        max_len = 0
        for line in self._korpus:
            for word in line.split(" "):
                index += 1
                stripped = word.strip(STRIPPER).lower()
                if stripped != "":
                    if stripped not in words:
                        words[stripped] = [index]
                    else:
                        words[stripped].append(i)
                    index += len(word)
            index += len(line)
        
        self._links = Links()
        
        with open(filename, encoding="UTF-8", mode="wt") as f:
            for word in sorted(words):'
                pass
                #f.write(str(lazy_hash(k,3)) + " " + str(k[4:]))
                #f.write(word + "\n")
                #f.write(str(len(t[1])) + " " + t[0] + "\n")
    
    def __getitem__(self, key):
        if key is not str:
            raise TypeError
        low, high = self._hash[key]
        while low < high:
            mid = (high - low)/2
            if self._index[mid] < key:
                low  = mid
            else:
                high = mid
        return self._links[low]


