import matplotlib.pyplot as plt
import numpy as np

def pieChart(dict):
    yv = dict.values()
    x = dict.keys()
    y = []
    for a in yv:
        y.append(len(a))
    fig, ax = plt.subplots()
    ax.axis('equal')
    patchers,text,autotext = ax.pie(y, radius=1.3, labels=x, colors=np.random.rand(3,4),autopct='%d%%' )
    for i in range(0, len(text)):
        text[i].set_color('white')

    return fig

def lineChart(dict,stringX,stringY):
    x = dict.keys()
    yv = dict.values()
    y =[]
    for a in yv:
        y.append(len(a))
    plt.plot(x,y,'w-')
    plt.xticks(x)
    plt.ylabel(stringY, {'color': 'white'})
    plt.xlabel(stringX, {'color': 'white'})
    return plt

def barChart(dict,stringX,stringY):
    x = dict.keys()
    y_plot = np.arange(len(x))
    yv = dict.values()
    y = []
    for a in yv:
        y.append(len(a))
    plt.bar(y_plot, y, align='center', alpha=1)
    plt.xticks(y_plot, x)
    ax = plt.subplot()
    plt.ylabel(stringY,{'color':'white'})
    plt.xlabel(stringX, {'color':'white'})

    for i in ax.spines:
        ax.spines[i].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    return plt
