from list import *
import re

def getArrayFromList(list):
    topic = []
    for s in list:
        s = s.lower()
        for w in politic:
            match = re.findall(w.lower(),s)
            if match:
                topic.append("politic")
        for w in sports:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("sports")
        for w in travel:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("travel")
        for w in spending:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("spending")
        for w in technology:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("technology")
        for w in education:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("education")
        for w in society:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("society")
    return topic

def getArrayFromString(string):
    sentence = string.split()
    topic = []
    for s in sentence:
        s = s.lower()
        for w in politic:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("politic")
        for w in sports:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("sports")
        for w in travel:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("travel")
        for w in spending:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("spending")
        for w in technology:
            match = re.findall(w.lower(), s)
            if match:
                print w
                topic.append("technology")
        for w in education:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("education")
        for w in society:
            match = re.findall(w.lower(), s)
            if match:
                topic.append("society")
    return topic


# print getArrayFromString(test)