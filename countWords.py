from __future__ import division

wordInsentence = []

### Sentence is a string e.g (hari ini hari sabtu
### key is keyword (hari)

def count(sentence, key):

    total = 0
    for a in sentence.split():
        if a == key:
            total = total + 1
    totalWords = len(sentence.split())
    percentage = (float(total / totalWords)) * 100
    return percentage
