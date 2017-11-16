from __future__ import division


# Sentence HAS to be a LIST
wordsDictionaryFreq = {}
words = []

list = {
    "kd puuru busuk", "raam busuk", "messi busuk sangat", "dian comel", "hari ini hari busuk", "hari hari hari jumaat"
}
def freqDictionary(list):

    for line in list:
        for w in line.split():
            words.append(w.lower())


    for w in words:
        count = 0
        for w2 in words:
            if w2 == w:
                count = count + 1
        wordsDictionaryFreq[w] = count

    return wordsDictionaryFreq

# Kasi List and keywords
def getPercentage(key,list):
    freqDictionary(list)
    totalkey = wordsDictionaryFreq.get(key)
    totalw = sum(wordsDictionaryFreq.values())
    percent = (totalkey/totalw)*100
    return percent
