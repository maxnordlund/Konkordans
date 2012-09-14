#!/usr/bin/env python3

import struct 

class Links:
    """En klass som pratar med filen med alla ords offseter"""
    def __init__(self, f):
        self._file = f

    def build(self, words):
        range_mapping = []

        self._file.seek(0)
        for word in sorted(words):
            indices = words[word]
            format_string = str(len(indices)) + "I"

            start = self._file.tell()
            range_mapping.append( (word, start, len(indices)) )

            chunk = struct.pack(format_string, *indices)

            self._file.write(chunk)

        return range_mapping

    def get(self, offset, length):
        self._file.seek(offset, 0) # find the index position
        data = self._file.read(length*4)
        format_string = str(length) + "I"
        return struct.unpack(format_string, data)


