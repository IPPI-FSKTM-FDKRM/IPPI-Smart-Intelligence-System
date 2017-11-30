
import matplotlib.pyplot as plt
import numpy as np

test = {"tuu":[1,1],"mama":[1,4,2]}
def pieChart(dict):
    yv = dict.values()
    x = dict.keys()
    y = []
    for a in yv:
        y.append(len(a))
    fig, ax = plt.subplots()
    ax.axis('equal')
    ax.pie(y, radius=1.3, labels=x, colors=['gold', 'lightskyblue', 'lightcoral'],autopct='%d%%' )
    plt.show()

def lineChart(dict,stringX,stringY):
    x = dict.keys()
    yv = dict.values()
    y =[]
    for a in yv:
        y.append(len(a))
    plt.plot(x,y,'k-')
    plt.xticks(x)
    plt.xlabel(stringX)
    plt.ylabel(stringY)
    plt.show()

def barChart(dict,stringX,stringY):
    x = dict.keys()
    y_plot = np.arange(len(x))
    yv = dict.values()
    y = []
    for a in yv:
        y.append(len(a))
    plt.bar(y_plot, y, align='center', alpha=0.5)
    plt.xticks(y_plot, x)
    plt.ylabel(stringY)
    plt.xlabel(stringX)
    plt.show()

pieChart(test)