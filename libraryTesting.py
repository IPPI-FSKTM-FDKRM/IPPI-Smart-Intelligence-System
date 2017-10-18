from __future__ import division
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from nltk.tokenize import word_tokenize
from list import words
sentiment_dictionary = {}

#Ambik words dari list
for line in words:
        #Split score according to List
        wordInsideDictionary, score = line.split('\t')
        sentiment_dictionary[wordInsideDictionary] = int(score)
#### Testing method return array of TOTAL negative and positive of A STRING eg [4,-6], NEGATIVE IS ALWAYS IN NEGATIVE NUMBER
def testing(string):

    pos = 0
    neg = 0
    for s in word_tokenize(string):
        val = sentiment_dictionary.get(s,0)
        if val > 0:
            pos+=val
        if val < 0:
            neg+=val

    return pos,neg

    textfile.close()
############### write in file ############
'''
def writingFile(newWords):
    writeFile = open('C:/Users/musfirah/Desktop/AFINN/AFINN-111.txt','a')
    check = sentiment_dictionary.get(newWords,0)
    if check == 0:
        wValue = raw_input('rate how positive/negative i am between [+5,+1] or [-1,-5] ONLY:')
        writeFile.write(newWords)
        writeFile.write('\t')
        writeFile.write(wValue)
        writeFile.write('\n')
    else:
        print "Perkataan dah exist in dictionary, try again"
'''''
