from nBayesTesting import *
import matplotlib.pyplot as plt

# Testing Data
#pos = open('C:/Users/musfirah/Desktop/positiveTesting.txt','r')
#neu = open('C:/Users/musfirah/Desktop/neutralTesting.txt','r')
'''''''''
# Pie Chart for sentiment
data = dictSent(neu)
y = data.values()
x = data.keys()
fig, ax = plt.subplots()
ax.axis('equal')
ax.pie(y, radius=1.3, labels=x, colors=['gold', 'lightskyblue', 'lightcoral'] )
plt.show()
'''''
# Line Graph for per post
# Test Data
test = {0:['a','b','c','d'],1:['e','f','g'],2:['h','i'],3:['j','k','l','m'],4:['n','o','p','q','r','s','t'],5:['u'],6:['v','w','x','y','z'],7:['a','b','c','d'],8:['v','w','x','y','z'],9:['v','w','x','y'],10:['v','w'],11:['v','w','x','y','z'],12:['v','w','x','y','z'],13:['v','w','x','y','z'],14:[],15:[],16:['v'],17:['v','w','x','y','z','1','2'],18:['v','w','x','y','z'],19:['v','w','x','y','z'],20:['v','w','x','y','z'],21:['v','w','x','y','z'],22:['v','w','x','y','z'],23:['v','w','x','y','z'],24:['v','w','x','y','z']}
x = test.keys()
yv = test.values()
y =[]
for a in yv:
    y.append(len(a))
plt.plot(x,y,'k-')
plt.xticks(x)
plt.xlabel("Hours")
plt.ylabel("Num of Post")
plt.show()

