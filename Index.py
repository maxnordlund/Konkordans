#!/usr/bin/env python3

import struct
import Links.Links as Links
import Hash.Hash as Hash

ENCODING = "ISO-8859-1" # Every character is 1 byte

class Index:
    """En klass som pratar med indexfilen"""
    def __init__(self, korpus, index_path="index.dat", link_path="links.dat"):
        self.chunk_size  = 0
        self._korpus     = korpus
        self._index_path = index_path
        self._link_path  = link_path
        self._hash       = None
        self._links      = None
    
    def __enter__(self):
        self._links_file = open(self._link_path,  mode="r+b")
        self._fil = open(self._index_path, mode="r+b", encoding=ENCODING))
        self._fil.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._fil.__exit__(exc_type, exc_val, exc_tb)
    
    def build(self):
        # Reading all words from our korpus
        index   = self._korpus.tell()
        words   = {}
        longest_word = 0
        for line in self._korpus:
            for word in line.split(" "):
                index += 1
                stripped = word.strip(STRIPPER).lower()

                if stripped == "": # Don't add strange empty words
                    continue

                if stripped not in words:
                    words[stripped] = [index]
                else:
                    words[stripped].append(i)
                index += len(word)
                longest_word = max(longest_word, len(word))
            index += len(line)
        
        # Building our index files

        # Build the word Links index file
        self._links = Links(self._links_file)
        range_mapping = self._links.build(words) 
        # from Links: (word, offset, size)

        # Build the main Index file
        word_indices = [] # To be added to the Hash index

        format_string = str(longest_word) + "sII"
        self.chunk_size = struct.calcsize(format_string)
        for word, rstart, rstop in range_mapping:
            word_indices.append(word, f.tell())
            
            # pack the data as bytes
            wordbytes = bytes(word.rjust(longest_word), encoding=ENCODING)
            chunk = struct.pack(format_string, wordbytes, rstart, rstop)

            self._fil.write(chunk)

        # Build the Hash index file
        self._hash = Hash("hash.dat", word_indices) 
    
    def __getitem__(self, key):
        if not self._hash:
            self._hash = Hash("hash.dat") 

        if key is not str:
            raise TypeError
        low, high = self._hash[key]
        format_string = str(longest_word) + "s"
        while low < high:
            mid = (high - low)/2
            mid = mid - mid % self.chunk_size
            self._fil.seek(mid, 0)
            data = self._fil.read(self.chunk_size)
            values = struct.unpack(format_string, data)
            if values[0] < key:
                low  = mid
            else:
                high = mid

        self._fil.seek(low, 0)
        data = self._fil.read(self.chunk_size)
        values = struct.unpack(format_string, data)
        return self._links.get(values[1], values[2])


