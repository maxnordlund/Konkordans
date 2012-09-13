#!/usr/bin/env python3

ISO = "ISO-8859-1"

class Korpus:
    """En klass som pratar med korpusen"""
    def __init__(self, path):
        self._path = path
    
    def __enter__(self):
        self._fil = open(self._path, encoding=ISO).__enter__() # Options?
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._fil.__exit__(exc_type, exc_val, exc_tb)
    
    def tell(self):
        return self._fil.tell()
        
    def __iter__(self):
        return self._fil.__iter__()
    
    def __len__(self):
        if self._len == None:
            self._len = self._fil.seek(0, SEEK_END)
        return self._len
    
    def __getitem__(self, key):
        string = ""
        if key is slice:
            if key.stop == None:
                self._fil.seek(key.start, SEEK_SET)
                string = self._fil.readline()
            else:
                start = 0
                stop  = 0
                if key.step != None:
                    start = key.step  - key.start
                    stop  = key.start + key.step
                    
                    start = start if start > 0 else 0
                    stop  = stop  if stop  > len(self) else len(self)
                else:
                    start = key.start
                    stop  = key.stop
                
                self._fil.seek(start, SEEK_SET)
                string = self._fil.read(stop)
        else:
            self._fil.seek(key, SEEK_SET)
            string = self._fil.readline().split()[0]
        return string
