
import matplotlib.pyplot as plt
import numpy as np

def pieChart(dict):
    plt.figure()
    yv = dict.values()
    x = dict.keys()
    y = []
    plt.figure()
    for a in yv:
        y.append(len(a))
    fig, ax = plt.subplots()
    ax.axis('equal')
    patches,text, autotext = ax.pie(y, radius=1.3, labels=x, colors=np.random.rand(3,4),autopct='%d%%')
    for i in range(0,len(text)):
        text[i].set_color('white')
    return plt

def pieChartSentiment(dict):

    yv = dict.values()
    x = dict.keys()
    y = []
    for a in yv:
        y.append(len(a))
    plt.figure()
    fig, ax = plt.subplots()
    ax.axis('equal')
    patches,text, autotext = ax.pie(y, radius=1.3, labels=x, colors=['lightgreen','gold','lightcoral'],autopct='%d%%')
    for i in range(0,len(text)):
        text[i].set_color('white')
    return plt


def lineChartTime(dict,stringX,stringY):
    newdict = {}
    for key in dict.keys():
        nkey = int(key.encode('utf=8'))
        newdict[nkey] = len(dict.get(key))
    for time in range (0,24):
        if newdict.get(time)==None:
            newdict[time] = 0
    x = newdict.keys()
    y = newdict.values()
    plt.figure()
    plt.plot(x,y,'w-')
    plt.xticks(x)
    plt.xlabel(stringX,{'color':'white'})
    plt.ylabel(stringY,{'color':'white'})
    ax = plt.subplot()
    for i in ax.spines:
        ax.spines[i].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    return plt

def lineChart(dict,stringX,stringY):
    a = sorted(dict.iterkeys())
    for key in a:
        dict[key] = dict.get(key)
    x = dict.keys()
    yv = dict.values()
    y =[]
    for a in yv:
        y.append(len(a))
    plt.figure()
    plt.plot(x,y,'w-')
    plt.xticks(x)
    plt.xlabel(stringX,{'color':'white'})
    plt.ylabel(stringY,{'color':'white'})
    ax = plt.subplot()
    for i in ax.spines:
        ax.spines[i].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    return plt

def barChartTime(dict,stringX,stringY):
    newdict = {}
    for key in dict.keys():
        nkey = int(key.encode('utf=8'))
        newdict[nkey] = len(dict.get(key))
    for time in range(0, 24):
        if newdict.get(time) == None:
            newdict[time] = 0
    x = newdict.keys()
    y = newdict.values()
    plt.figure()
    y_plot = np.arange(len(x))
    plt.ylim((min(y)+0.5),(max(y)+0.5))
    bar = plt.bar(y_plot, y, align='center')
    for i in range(0,len(bar)):
       bar[i].set_color("white")
    plt.xticks(y_plot, x)
    ax = plt.subplot()
    ax.set_ylim(ymin=0)
    plt.ylabel(stringY,{'color':'white'})
    plt.xlabel(stringX,{'color':'white'})
    for i in ax.spines:
        ax.spines[i].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    return plt

def barChart(dict,stringX,stringY):
    plt.figure()
    x = dict.keys()
    plt.figure()
    y_plot = np.arange(len(x))
    yv = dict.values()
    y = []
    for a in yv:
        y.append(len(a))
    plt.ylim((min(y)+0.5),(max(y)+0.5))
    bar = plt.bar(y_plot, y, align='center')
    for i in range(0,len(bar)):
       bar[i].set_color("white")
    plt.xticks(y_plot, x)
    plt.ylim(min(y),max(y))
    ax = plt.subplot()
    plt.ylabel(stringY,{'color':'white'})
    plt.xlabel(stringX,{'color':'white'})
    for i in ax.spines:
        ax.spines[i].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    return plt
