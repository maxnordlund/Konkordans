#!/usr/bin/env python3

words = set()

with open("korpus", encoding="ISO-8859-1") as f:
    for line in f:
        for word in line.split():
            words.add(word.strip("!\"%&'()*+,-./0123456789:;=?_€§©®·[]$<>@`").lower())

with open("ut", encoding="UTF-8", mode="wt") as f:
    for word in sorted(words):
        f.write(word + "\n")
