#!/usr/bin/env python3

import struct
import Links
import Hash

ENCODING = "ISO-8859-1" # Every character is 1 byte
STRIPPER   = "\"\n\t!%&'()*+,-./0123456789:;=?_€§¤©®·°[]$<>@´`"

class Index:
    """En klass som pratar med indexfilen"""
    def __init__(self, korpus, index_path="index.dat", link_path="links.dat"):
        self.chunk_size   = 0
        self.word_len = 0
        self._korpus     = korpus
        self._index_path = index_path
        self._link_path  = link_path
        self._hash       = None
        self._links      = None
        self._fil = None
    
    def __enter__(self):
        #self._fil = open(self._index_path, mode="wb")#, encoding=ENCODING)
        #self._fil.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._fil:
            return self._fil.__exit__(exc_type, exc_val, exc_tb)
    
    def parse_korpus(self, filename):
        f = open(filename, "rb")

        index = 0
        line = f.readlines(1)
        words   = {}
        word_len = 0
        while line != []:
            for word in line[0].split(b' '):
                word = word.decode(ENCODING).strip(STRIPPER).lower()
                if word=="australien":
                    aus = index
                if word == "": # Don't add strange empty words
                    continue
                elif word not in words:
                    words[word] = [index]
                    word_len = max(word_len, len(word))
                else:
                    words[word].append(index)
                index += len(word) + 1

            index = f.tell()
            line = f.readlines(1)

        f.close()

        return words, word_len

    def write(self, filename, words, word_len):
        # Build the main Index file
        self._fil = open(filename, mode="wb")

        format_string = str(word_len) + "sII"
        self.chunk_size = struct.calcsize(format_string)
        chunk = struct.pack("I", word_len)
        self._fil.seek(0)
        self._fil.write(chunk)

        word_indices = [] # To be added to the Hash index
        for word, start, length in sorted(words):
            word_indices.append( (word, self._fil.tell()) )
            
            # pack the data as bytes
            wordbytes = bytes(word.ljust(word_len), encoding=ENCODING)
            chunk = struct.pack(format_string, wordbytes, start, length)

            self._fil.write(chunk)
        self._fil.close()
        return word_indices

    def build(self):
        # Reading all words from our korpus
        words, word_len = self.parse_korpus("/info/adk12/labb1/korpus")
        print("Läst alla ord..")

        self.word_len = word_len

        # Build the word Links index file
        links_words = [] # from Links: (word, offset, size)
        with open(self._link_path,  mode="wb") as f:
            self._links = Links.Links(f)
            links_words = self._links.build(words) 

        # Build the main Index file
        word_indices = self.write(self._index_path, links_words, self.word_len)

        # Build the Hash index file
        self._hash = Hash.Hash("hash.dat", word_indices) 
    
    def __getitem__(self, key):
        if type(key) is not str:
            raise TypeError

        if not self._hash:
            self._hash = Hash.Hash("hash.dat") 
        format_string=""
        if self.chunk_size == 0:
            self._fil = open(self._index_path, mode="rb")
            data = self._fil.read(4)
            self.word_len = struct.unpack("I", data)[0] 
            format_string = str(self.word_len) + "sII"
            self.chunk_size = struct.calcsize(format_string)

        low, high = self._hash[key]
        i = 0
        while low < high and i < 12:
            i += 1
            mid = int((high + low)/2)
            mid = mid - (mid % self.chunk_size)
            self._fil.seek(mid+4, 0)
            data = self._fil.read(self.chunk_size)
            values = struct.unpack(format_string, data)
            word = values[0].decode(ENCODING).strip()
            if word < key:
                low  = mid + self.chunk_size
            elif word > key:
                high = mid - self.chunk_size
            else:
                break # Found it!

        self._fil.seek(mid+4, 0)
        data = self._fil.read(self.chunk_size)
        word, offset, length = struct.unpack(format_string, data)
            
        with open(self._link_path,  mode="rb") as f:
            self._links = Links.Links(f)
            return self._links.get(offset, length)


def sparad():
        words   = {}
        word_len = 0
        lines = self._korpus._fil.readline()
        index_a = 0
        for line in self._korpus._fil:
            index = index_a
            index_a += len(line)
            for word in line.split(b" "):
                index += 1
                index += len(word)
                stripped = word.decode(ENCODING).strip(STRIPPER).lower()
                
                if stripped == "australien":
                    print(index, line[index-index_a:index-index_a+20])

                if stripped == "": # Don't add strange empty words
                    continue

                if stripped not in words:
                    words[stripped] = [index]
                else:
                    words[stripped].append(index)
                word_len = max(word_len, len(word))
            index += len(line)
            line = self._korpus._fil.readline(1)
        
