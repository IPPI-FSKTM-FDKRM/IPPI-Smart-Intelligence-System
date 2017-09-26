from nltk.tokenize import word_tokenize

sentiment_dictionary = {}

textfile = open('C:/Users/musfirah/Desktop/AFINN/AFINN-111.txt')
for line in textfile:
        wordInsideDictionary, score = line.split('\t')
        sentiment_dictionary[wordInsideDictionary] = int(score)

def testing():


    sentence = raw_input("Tulis sini :")
    wordsInSentence = word_tokenize(sentence)

    ######### print positive negative seperately ###################

    pos = 0
    neg = 0
    for s in word_tokenize(sentence):
        val = sentiment_dictionary.get(s,0)
        if val > 0:
            pos+=val
        if val < 0:
            neg+=val

    print "positive value:",pos,"negative value:",neg

    textfile.close()
############### write in file ############

def writingFile():
    print "masuk"
    writeFile = open('C:/Users/musfirah/Desktop/AFINN/AFINN-111.txt','a')
    newWords = raw_input("perkataan baru(ajar yang baik baik ya): ")
    check = sentiment_dictionary.get(newWords,0)
    if check == 0:
        wValue = raw_input('rate how positive/negative i am between [+5,+1] or [-1,-5] ONLY:')
        writeFile.write(newWords)
        writeFile.write('\t')
        writeFile.write(wValue)
        writeFile.write('\n')
    else:
        print "Perkataan dah exist in dictionary, try again"


print("Hai nak test or input new word? 1 = test, 2 = new word, 0 quit")
val = raw_input(">>")
while val !="0":
    if val == "1":
        testing()
    if val == "2":
        writingFile()
    print("Hai nak test or input new word? 1 = test, 2 = new word, 0 quit")
    val = raw_input(">>")

