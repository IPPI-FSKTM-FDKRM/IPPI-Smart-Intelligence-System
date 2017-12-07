import matplotlib.pyplot as plt
import numpy as np

def pieChart(dict,color):
    yv = dict.values()
    x = dict.keys()
    y = []
    for a in yv:
        y.append(len(a))
    fig, ax = plt.subplots()
    ax.axis('equal')
    patches,text, autotext = ax.pie(y, radius=1.3, labels=x, colors=np.random.rand(5,3),autopct='%d%%')
    for i in range(0,len(text)):
        text[i].set_color(color)
    return plt

def pieChartSentiment(dict,color):
    yv = dict.values()
    x = dict.keys()
    y = []
    for a in yv:
        y.append(len(a))
    fig, ax = plt.subplots()
    ax.axis('equal')
    patches,text, autotext = ax.pie(y, radius=1.3, labels=x, colors=['lightskyblue','gold','lightcoral'],autopct='%d%%')
    for i in range(0,len(text)):
        text[i].set_color(color)
    return plt

def lineChartTime(dict,stringX,stringY,color):
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
    plt.xlabel(stringX,{'color':color})
    plt.ylabel(stringY,{'color':color})
    ax = plt.subplot()
    for i in ax.spines:
        ax.spines[i].set_color(color)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    return plt
def lineChart(dict,stringX,stringY,color):
    x = dict.keys()
    yv = dict.values()
    y =[]
    for a in yv:
        y.append(len(a))
    plt.figure()
    plt.plot(x,y,'w-')
    plt.xticks(x)
    plt.xlabel(stringX,{'color':color})
    plt.ylabel(stringY,{'color':color})
    ax = plt.subplot()
    for i in ax.spines:
        ax.spines[i].set_color(color)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    return plt

def barChartTime(dict,stringX,stringY,color):
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
       bar[i].set_color(color)
    plt.xticks(y_plot, x)
    ax = plt.subplot()
    ax.set_ylim(ymin=0)
    plt.ylabel(stringY,{'color':color})
    plt.xlabel(stringX,{'color':color})
    for i in ax.spines:
        ax.spines[i].set_color(color)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    return plt

def barChart(dict,stringX,stringY,color):
    plt.figure()
    x = dict.keys()
    y_plot = np.arange(len(x))
    yv = dict.values()
    y = []
    for a in yv:
        y.append(len(a))
    plt.ylim((min(y)+0.5),(max(y)+0.5))
    bar = plt.bar(y_plot, y, align='center')
    for i in range(0,len(bar)):
       bar[i].set_color(color)
    plt.xticks(y_plot, x)
    ax = plt.subplot()
    plt.ylabel(stringY,{'color':color})
    plt.xlabel(stringX,{'color':color})
    for i in ax.spines:
        ax.spines[i].set_color(color)
    ax.xaxis.label.set_color(color)
    ax.yaxis.label.set_color(color)
    ax.tick_params(axis='x', colors=color)
    ax.tick_params(axis='y', colors=color)
    return plt
