#!/usr/bin/env python3

import struct
import Links, Hash
import math
from os import SEEK_SET

ENCODING = "ISO-8859-1" # Every character is 1 byte
STRIPPER = "\"\n\t!%&'()*+,-./0123456789:;=?_€§¤©®·°[]$<>@´`"

# alfabet i Latin-1-ordning 
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÅÖ"

def makeTable():
    a = ord('a')
    A = ord('A')
    till = bytearray(' ' * 256, ENCODING)
    från = bytearray(range(256))
    
    for s in ALPHABET:
        ch = ord(s) + a - A
        till[ord(s)] = till[ch] = ch

    # Nedan följer speciallösning för att klara accenterade tecken
    
    for ch in range(224, 227+1): # a med accent (utillm å och ä) 
        till[ch +  - a + A] = till[ch] = a
    
    ch = 230 # ae till ä 
    till[ch +  - a + A] = till[ch] = ord('ä')
    
    ch = 231 # c med cedilj till c
    till[ch +  - a + A] = till[ch] = ord('c')
    
    for ch in range(232, 235+1): # e med accent (även é) 
        till[ch +  - a + A] = till[ch] = ord('e')
        
    for ch in range(236, 239+1): # i med accent 
        till[ch +  - a + A] = till[ch] = ord('i')
        
    ch = 241 # n med ~ rill n 
    till[ch +  - a + A] = till[ch] = ord('n')
    
    for ch in range(242, 245+1): # o med accent (förutillm ö) 
        till[ch +  - a + A] = till[ch] = ord('o')
        
    ch = 248 # o genomskuret till ö 
    till[ch +  - a + A] = till[ch] = ord('ö') 
    
    for ch in range(249, 252+1): # u med accent 
        till[ch +  - a + A] = till[ch] = ord('u')
        
    ch = 253 # y med accent 
    till[ch +  - a + A] = till[ch] = ord('y')
    ch = 255
    till[ch +  - a + A] = till[ch] = ord('y')
    
    return bytes.maketrans(från, till)

TRANSLATE = makeTable()

class Index:
    """En klass som pratar med indexfilen"""
    def __init__(self, korpus, index_path="index.dat", link_path="links.dat"):
        self.chunk_size  = 0
        self.word_len    = 0
        self._korpus     = korpus
        self._index_path = index_path
        self._link_path  = link_path
        self._hash       = None # Handler for the Hash index
        self._links      = None # Handler for the Links index
        self._index      = None # File containing the main Index
    
    def __enter__(self):
        #self._index = open(self._index_path, mode="r+b")#, encoding=ENCODING)
        #self._index.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._index:
            return self._index.__exit__(exc_type, exc_val, exc_tb)
    
    def parse_korpus(self, filename):
        """Returns a list of (hash, string, indices)-tuples."""
        with open(filename, "rb") as f:
            words   = {}
            index = 0
            longest_word = 0
            line = f.readlines(1)
            while line != []:
                line = line[0].translate(TRANSLATE).decode(ENCODING)
                for word in line.split(" "):
                    index += len(word) + 1
                    if word == "": # Don't add strange empty words
                        continue
                    elif word not in words:
                        words[word] = [index]
                        longest_word = max(longest_word, len(word))
                    else:
                        words[word].append(index)
                index = f.tell()
                line = f.readlines(1)
            
            lazy = Hash.lazy_hash
            word_list = [(lazy(w), w, words[w]) for w in words]
            word_list = sorted(word_list, key=lambda t: t[1])
            word_list = sorted(word_list, key=lambda t: t[0])

            return word_list, longest_word

    def build(self):
        # Reading all words from our korpus
        words, word_len = self.parse_korpus("/info/adk12/labb1/korpus")
        print("Läst alla ord..")

        self.word_len = word_len
        
        # Build the word Links index file
        links_words = [] 
        with open(self._link_path,  mode="wb") as f:
            self._links = Links.Links(f)
            links_words = self._links.build(words) # from Links: (word, offset, size)

        # Build the main Index file
        word_indices = self.write(self._index_path, links_words, self.word_len)

        # Build the Hash index file
        self._hash = Hash.Hash("hash.dat", word_indices) 

    def write(self, filename, words, word_len):

        # Build the main Index file
        word_indices = [] # To be added to the Hash index
        self.format_string = str(word_len) + "sII"
        self.chunk_size = struct.calcsize(self.format_string)

        with open(filename, mode="wb") as f:
            # header
            f.seek(0)
            f.write(struct.pack("I", word_len)) 

            for word, start, length in words:
                word_indices.append( (word, f.tell()) )
                
                # pack the data as bytes
                wordbytes = bytes(word.rjust(word_len), encoding=ENCODING)
                chunk = struct.pack(self.format_string, wordbytes, start, length)

                f.write(chunk)
        #self._index.close()
        return word_indices

    
    def __getitem__(self, key):
        if type(key) is not str:
            raise TypeError

        with open(self._index_path, mode="rb") as self._index:
            # read header
            self.word_len = struct.unpack("I", self._index.read(4))[0]
            self.format_string = str(self.word_len) + "sII"
            self.chunk_size = struct.calcsize(self.format_string)
            self._index

            # Get word list boundaries
            low, high = Hash.Hash("hash.dat")[key]
            # Get the offset and length of the index list
            offset, length = self.binary_search(key, low, high)

        with open(self._link_path,  mode="rb") as f:
            return Links.Links(f).get(offset, length)

    def binary_search(self, key, low, high):
        def read_chunk(start):
            start = start - (start % self.chunk_size)
            self._index.seek(start+4, SEEK_SET) # +4 from header size
            data = self._index.read(self.chunk_size)
            word, offset, length = struct.unpack(self.format_string, data)
            word = word.decode(ENCODING).strip()
            return word, offset, length
        
        if high == low: # Sentinel in case low == high
            _, offset, length = read_chunk(high)
            return offset, length
        
        i = 0       # Sentinel against infinite loops
        ordo = math.log(high-low,2) + 1
        while low < high and i < ordo:
            i += 1
            mid = int((high + low)/2)

            word, offset, length = read_chunk(mid)
            
            if word < key:
                low = mid
                #low  = mid + self.chunk_size
            elif word > key:
                high = mid
                #high = mid - self.chunk_size
            else: # word == key
                break # Found it!
        else:
            raise Exception("Ordet finns inte i indexet.", key)

        return offset, length


