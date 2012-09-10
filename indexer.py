#!/usr/bin/env python3

from collections import OrderedDict

# Läs en byte med högst en inläsning från disk
read = lambda f: f.read(1).decode(encoding="ISO-8859-1").lower() 
peek = lambda f: f.peek(1).decode(encoding="ISO-8859-1").lower() 

words = {}

# Öppna rwb för att kunna fråga om var man är.
strip_characters = "!\"%&'()*+,-./0123456789:;=?_€§©®·[]$<>@`"

with open("korpus", mode="r+b") as f:
    c = read(f)
    s = bytearray()
    begining = f.tell()
    while f.readable():
        p = peek(f)
        if c.isalnum() or not p.isspace():
            s.extend(c.encode(encoding="ISO-8859-1"))
        if p.isspace():
            s = s.decode(encoding="ISO-8859-1")
            if s not in words:
                words[s] = [begining]
            else:
                words[s].append(begining)
            s = bytearray()
            begining = f.seek(1, SEEK_CUR)
        c = p

words = OrderedDict(sorted(d.items(), key=lambda t: t[0]))

with open("ut", encoding="UTF-8", mode="wt") as f:
    for t in words.items():
        f.write(t[0] + " " + t[1] + "\n")

