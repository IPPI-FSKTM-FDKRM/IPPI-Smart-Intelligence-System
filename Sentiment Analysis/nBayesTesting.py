from __future__ import division
import decimal

############################################################################################################################
#           Nak Pakai Seru getListValue --> terima list of sentence = sentence = {"messi busuk", "raam busuk", "kd busuk"} #
#                           Dia akan return list = [Positive, Negative,Neutral,Positive,..]                                #
############################################################################################################################
trainDictPos = open('C:/Users/musfirah/Desktop/posDictionary.txt','r')
trainDictNeg = open('C:/Users/musfirah/Desktop/negDictionary.txt','r')
trainDictNeu = open('C:/Users/musfirah/Desktop/neuDictionary.txt','r')

# transfer link to dictionary
def dictionary(link):
    d = {}
    for line in link:
        word, val = line.split(" ")
        d[word] = val
    return d

dPos = dictionary(trainDictPos)
dNeg = dictionary(trainDictNeg)
dNeu = dictionary(trainDictNeu)


#compare text with dictionary

def getVal(text,dict):
    d = dict
    value = 0
    for w in text.split():
        w = w.lower()
        if d.has_key(w):
            value = value + decimal.Decimal(d.get(w))
    return value



def getListValue(linktest):
    val = []
    for line in linktest:
        pV = getVal(line, dPos)
        nV = getVal(line, dNeg)
        neuV = getVal(line, dNeu)

        if pV > nV:
            if pV > neuV:
                val.append("positive")
            else:
                val.append("neutral")
        else:
            if nV > neuV:
                val.append("negative")
            else:
                val.append("neutral")
    return val

'''''''''
def getAccuracy(list,t):
    count = 0
    for v in list:
        if v == t:
            count = count + 1
    return (count / len(list)) * 100
'''






###############################
##UPDATE FOR LEARNING PURPOSE##
###############################
