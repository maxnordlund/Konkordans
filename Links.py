#!/usr/bin/env python3

import struct 

class Links:
    """En klass som pratar med filen med alla ords offseter"""
    def __init__(self, f):
        self._links = f

    def build(self, words):
        links = []

        self._links.seek(0)
        for word in sorted(words):
            indices = words[word]
            format_string = str(len(indices)) + "I"

            start = self._links.tell()
            links.append( (word, start, len(indices)) )

            chunk = struct.pack(format_string, *indices)

            self._links.write(chunk)

        return links

    def get(self, offset, length):
        self._links.seek(offset, 0) # find the index position
        data = self._links.read(length*4)
        format_string = str(length) + "I"
        return struct.unpack(format_string, data)


