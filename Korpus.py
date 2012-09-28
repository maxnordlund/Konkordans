#!/usr/bin/env python3

import os
ENCODING = "ISO-8859-1"

class Korpus:
    """En klass som pratar med korpusen"""
    def __init__(self, path):
        self._path = path
        self._len = None
    
    def tell(self):
        return self._fil.tell()
    
    def readline(self):
        return self._fil.readlines(1)
    
    def __enter__(self):
        self._fil = open(self._path, "rb").__enter__() # Options?
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._fil.__exit__(exc_type, exc_val, exc_tb)
        
    def __iter__(self):
        return self._fil.__iter__()
    
    def __len__(self):
        if self._len == None:
            self._len = self._fil.seek(0, os.SEEK_END)
        return self._len
    
    def __getitem__(self, key):
        string = ""
        if type(key) is slice:
            # Called with a slice(offl, index, offr)
            if key.stop == None:
                self._fil.seek(key.start, os.SEEK_SET)
                string = self._fil.readline()
            else:
                start = 0
                stop  = 0
                if key.step != None:
                    start = key.stop - key.start
                    stop  = key.stop + key.step
                    
                    start = start if start > 0 else 0
                    stop  = stop  if stop  < len(self) else len(self)
                else:
                    start = key.start
                    stop  = key.stop
                size = stop - start
                self._fil.seek(start, os.SEEK_SET)
                string = self._fil.read(size)
        else:
            self._fil.seek(key, os.SEEK_SET)
            string = self._fil.readline().split()[0]
        return string
