#!/usr/bin/env python3

import struct 

class Links
    """En klass som pratar med filen med alla ords offseter"""
    def __init__(self, f):
        self._file = f

    def build(self, words):
        range_mapping = []

        self._file.seek(0)
        for word in sorted(words):
            indices = words[word]
            format_string = str(len(indices)+1) + "I"

            start = self._file.tell()
            chunk_size = struct.calcsize(format_string)
            range_mapping.append( (word, start, chunk_size) )

            chunk = struct.pack(format_string, *indices)
            self._file.write(chunk)

        return range_mapping

    def get(self, offset, size):
        self._file.seek(offset, 0) # find the index position
        data = self._file.read(size)
        format_string = "I"*(size / struct.calcsize("I") )
        return struct.unpack(format_string, data)

