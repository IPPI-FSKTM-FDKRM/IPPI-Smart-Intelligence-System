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
    patches,text, autotext = ax.pie(y, radius=1.3, labels=x, colors=np.random.rand(3,4),autopct='%d%%')
    for i in range(0,len(text)):
        text[i].set_color('white')
    return plt

def lineChart(dict,stringX,stringY):
    x = dict.keys()
    yv = dict.values()
    y =[]
    for a in yv:
        y.append(len(a))
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


def barChart(dict,stringX,stringY):
    x = dict.keys()
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

test = {u'1': [{u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-10-24T03:39:34+0000', u'message': u'Another day another life', u'story': u'Khairul Albertado Danial is at Faculty of Computer Science and Information Technology.', u'id': u'1362815530452737_1526135860787369'}], u'0': [{u'created_time': u'2017-10-16T12:44:58+0000', u'message': u'Hazim Kamaruzzaman Yeah manager', u'story': u"Khairul Albertado Danial shared Jawatankuasa Pelajar Luar Kampus Universiti Malaya's post.", u'id': u'1362815530452737_1519290884805200'}], u'2': [{u'created_time': u'2017-11-29T13:45:23+0000', u'story': u"Khairul Albertado Danial shared Marvel's video.", u'id': u'1362815530452737_1559916964075925'}, {u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}, {u'created_time': u'2017-11-08T11:11:00+0000', u'story': u"Khairul Albertado Danial shared Malaysians for Malaysia's post.", u'id': u'1362815530452737_1539802529420702'}, {u'created_time': u'2017-10-25T00:31:11+0000', u'story': u"Khairul Albertado Danial shared Oh My Media's video.", u'id': u'1362815530452737_1526977137369908'}], u'5': [{u'created_time': u'2017-10-28T15:56:39+0000', u'story': u"Khairul Albertado Danial shared Oh My Media's video.", u'id': u'1362815530452737_1530158793718409'}], u'4': [{u'created_time': u'2017-12-01T13:05:24+0000', u'story': u"Khairul Albertado Danial shared The Farigh Vines's video.", u'id': u'1362815530452737_1561929067208048'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-24T09:41:04+0000', u'message': u'Alhamdulillah , lots more to improve.. 1 more week towards integration. My team will do well... :Putnam:', u'story': u'Khairul Albertado Danial is at Kerinchi LRT station.', u'id': u'1362815530452737_1554649987935956'}, {u'created_time': u'2017-11-23T21:05:58+0000', u'message': u'Wish me luck for tomorrow', u'story': u'Khairul Albertado Danial is at Faculty of Computer Science and Information Technology.', u'id': u'1362815530452737_1554208991313389'}, {u'created_time': u'2017-10-27T12:38:23+0000', u'story': u'Khairul Albertado Danial shared a link.', u'id': u'1362815530452737_1529128583821430'}, {u'created_time': u'2017-10-20T14:49:00+0000', u'message': u'Listed on gartner trending hype', u'story': u"Khairul Albertado Danial shared Futurism's video.", u'id': u'1362815530452737_1523111661089789'}], u'6': [{u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}, {u'created_time': u'2017-11-18T19:54:37+0000', u'story': u"Khairul Albertado Danial shared GSCinemas's video.", u'id': u'1362815530452737_1549581305109491'}, {u'created_time': u'2017-11-18T18:57:43+0000', u'story': u"Khairul Albertado Danial shared Ali Roti Canai Tsunami's post.", u'id': u'1362815530452737_1549544638446491'}, {u'created_time': u'2017-11-18T18:57:36+0000', u'story': u"Khairul Albertado Danial shared Ali Roti Canai Tsunami's post.", u'id': u'1362815530452737_1549544518446503'}, {u'created_time': u'2017-11-05T07:18:08+0000', u'story': u"Khairul Albertado Danial shared Nas Daily's episode.", u'id': u'1362815530452737_1537037106363911'}, {u'created_time': u'2017-10-29T01:53:45+0000', u'story': u"Khairul Albertado Danial shared The Independent's video.", u'id': u'1362815530452737_1530568540344101'}],u'11': [{u'created_time': u'2017-11-29T13:45:23+0000', u'story': u"Khairul Albertado Danial shared Marvel's video.", u'id': u'1362815530452737_1559916964075925'}, {u'created_time': u'2017-11-29T06:43:04+0000', u'message': u'Last day at um academia community conference 2017', u'story': u'Khairul Albertado Danial is at Crystal Crown Hotel Petaling Jaya.', u'id': u'1362815530452737_1559629380771350'}, {u'created_time': u'2017-11-24T15:47:36+0000', u'message': u'Maybe we should change to iphone. Hafiz Redha Raam Kanaisan Aizat Rafee Amzar Mayfleet Chan', u'story': u'Khairul Albertado Danial is at Kolej Kediaman Kelapan,Universiti Malaya.', u'id': u'1362815530452737_1554897484577873'}, {u'created_time': u'2017-11-24T09:41:04+0000', u'message': u'Alhamdulillah , lots more to improve.. 1 more week towards integration. My team will do well... :Putnam:', u'story': u'Khairul Albertado Danial is at Kerinchi LRT station.', u'id': u'1362815530452737_1554649987935956'}, {u'created_time': u'2017-11-23T21:05:58+0000', u'message': u'Wish me luck for tomorrow', u'story': u'Khairul Albertado Danial is at Faculty of Computer Science and Information Technology.', u'id': u'1362815530452737_1554208991313389'}, {u'created_time': u'2017-11-21T07:59:28+0000', u'message': u'Irfan Kamaruddin Raam Kanaisan Hafiz Redha Aida Baharun, actually this is how alzheimer brain looks like , it is good to know about all this topic', u'story': u"Khairul Albertado Danial shared Dr John's video.", u'id': u'1362815530452737_1551861968214758'}, {u'created_time': u'2017-11-19T05:25:25+0000', u'message': u'Datang la support boling padang ulk pada 25/26 november', u'story': u'Khairul Albertado Danial is at Kompleks Sukan Negara Bukit Kiara.', u'id': u'1362815530452737_1549934008407554'}, {u'created_time': u'2017-11-18T19:54:37+0000', u'story': u"Khairul Albertado Danial shared GSCinemas's video.", u'id': u'1362815530452737_1549581305109491'}, {u'created_time': u'2017-11-18T18:57:43+0000', u'story': u"Khairul Albertado Danial shared Ali Roti Canai Tsunami's post.", u'id': u'1362815530452737_1549544638446491'}, {u'created_time': u'2017-11-18T18:57:36+0000', u'story': u"Khairul Albertado Danial shared Ali Roti Canai Tsunami's post.", u'id': u'1362815530452737_1549544518446503'}, {u'created_time': u'2017-11-08T11:27:17+0000', u'message': u'Main lawn bowl bersama Raam Kanaisan Irfan Kamaruddin dan Hazim Kamaruzzaman\n\n#FYPpurpose', u'story': u'Khairul Albertado Danial is with Raam Kanaisan and 2 others at Malaysian Lawn Bowls Federation.', u'id': u'1362815530452737_1539814052752883'}, {u'created_time': u'2017-11-08T11:11:00+0000', u'story': u"Khairul Albertado Danial shared Malaysians for Malaysia's post.", u'id': u'1362815530452737_1539802529420702'}, {u'created_time': u'2017-11-05T07:18:08+0000', u'story': u"Khairul Albertado Danial shared Nas Daily's episode.", u'id': u'1362815530452737_1537037106363911'}], u'10': [{u'created_time': u'2017-10-29T01:53:45+0000', u'story': u"Khairul Albertado Danial shared The Independent's video.", u'id': u'1362815530452737_1530568540344101'}, {u'created_time': u'2017-10-28T15:56:39+0000', u'story': u"Khairul Albertado Danial shared Oh My Media's video.", u'id': u'1362815530452737_1530158793718409'}, {u'created_time': u'2017-10-27T12:38:23+0000', u'story': u'Khairul Albertado Danial shared a link.', u'id': u'1362815530452737_1529128583821430'}, {u'created_time': u'2017-10-25T00:31:11+0000', u'story': u"Khairul Albertado Danial shared Oh My Media's video.", u'id': u'1362815530452737_1526977137369908'}, {u'created_time': u'2017-10-24T03:39:34+0000', u'message': u'Another day another life', u'story': u'Khairul Albertado Danial is at Faculty of Computer Science and Information Technology.', u'id': u'1362815530452737_1526135860787369'}, {u'created_time': u'2017-10-20T14:49:00+0000', u'message': u'Listed on gartner trending hype', u'story': u"Khairul Albertado Danial shared Futurism's video.", u'id': u'1362815530452737_1523111661089789'}, {u'created_time': u'2017-10-16T12:44:58+0000', u'message': u'Hazim Kamaruzzaman Yeah manager', u'story': u"Khairul Albertado Danial shared Jawatankuasa Pelajar Luar Kampus Universiti Malaya's post.", u'id': u'1362815530452737_1519290884805200'}], u'12': [{u'created_time': u'2017-12-01T13:05:24+0000', u'story': u"Khairul Albertado Danial shared The Farigh Vines's video.", u'id': u'1362815530452737_1561929067208048'}]}

f = barChart(test,"X","Y")
f.savefig("tt.png",transparent=True)
