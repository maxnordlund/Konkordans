#!/usr/bin/env python3

import pickle

mappings = [0]*256
for v, c in enumerate(range(ord('a'), ord('z')+1)):
    mappings[c] = v+1
mappings[ord('å')] = 27
mappings[ord('ä')] = 28
mappings[ord('ö')] = 29

def lazy_hash(word):
    """Hashes the first three letters of the word. """
    word = word.rjust(3)
    value  = mappings[ord(word[0])] * 900
    value += mappings[ord(word[1])] * 30
    value += mappings[ord(word[2])]
    return value
    

class Hash:
    """En klass som pratar med latmanshashindexfilen. Använder pickle för att spara och ladda informationen från fil."""
    def __init__(self, path):
        self._hashes = None
        with open(path, 'wb') as f:
            self._hashes = pickle.load(f)
        
    def __init__(self, path, word_indices=None):
        self._hashes = None

        if word_indices is None:
            with open(path, 'rb') as f:
                self._hashes = pickle.load(f)
        else:
            self.build(path, word_indices)

    def build(self, path, word_indices):
        """Constructs the Hash index from a list of words and offsets and saves it to file."""
        used_hashes = set()
        self._hashes = [0] * 27000 # prepopulate

        # set all existant hashes to their word indices
        for word, pos in word_indices:
            h = lazy_hash(word)
            if h not in used_hashes:
                used_hashes.add(h)
                self._hashes[h] = pos
        # let's save the index of the last word as well
        self._hashes.append( word_indices[-1][1] )

        # save our progress to file
        with open(path, "wb") as f:
            pickle.dump(self._hashes, f)

    def __getitem__(self, key):
        """Return the lower and higher indices for the search term."""
        h = lazy_hash(key)
        index_l = self._hashes[h]
        if index_l == 0:
            raise Exception("No index for hash('{}')={}".format(key, h))

        # Continue searching for the next term (guaranteed to exist)
        for index_h in self._hashes[h+1:]:
            if index_h != 0:
                return index_l, index_h

