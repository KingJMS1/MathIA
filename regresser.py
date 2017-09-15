import os   
from pylab import *
import numpy as np
import bokeh
from LoadGame import LoadGame
import scipy as sp

def removeOutliers(xdata, ydata, fencelow=None, fencehigh=None):
    if fencelow == None:
        iqr = sp.stats.iqr(ydata)
        median = sp.median(ydata)
        qthree = median + iqr/2
        qone = median - iqr/2
        fencelow = qone - 1.5*iqr
        fencehigh = qthree + 1.5*iqr
    index = 0
    flag = False
    for y in ydata:
        if y > fencelow and y < fencehigh:
            pass
        else:
            xdata.pop(index)
            ydata.pop(index)
            flag = True
            break
        index = index + 1
    if flag:
        return removeOutliers(xdata, ydata, fencelow, fencehigh)
    else:
        return (xdata, ydata)


datadir = os.path.abspath("D:/data/")
games = os.listdir(datadir)
games.remove("FakeGames")
fakelist = os.path.join(datadir, "FakeGames")
fakegame = "NotYet"
file = open(fakelist)
while(fakegame != ""):
    fakegame = file.readline().rstrip("\n")
    if fakegame != "":
        games.remove(fakegame)
for game in games:
    newpath = os.path.join(datadir, game)
    check = os.listdir(newpath)
    if "NEP" in check:
        games.remove(game)

xdata = []
ydata = []
print(games)
stat = "medians"

if stat == "contrast":
    for dirname in games:
        aname = os.path.join(datadir, dirname)
        print(aname)
        game = LoadGame(aname)
        xdata.append(np.median(game.stats["contrast"]))
        ydata.append(game.players)
    #xdata, ydata = removeOutliers(xdata, ydata)
    
    plot(xdata, ydata, 'ko')
    xlabel(stat.capitalize())
    ylabel("Players on Release")    
    title("Median " + stat.capitalize() + " vs Players")
    show()        
else:
    rxdata = []
    gxdata = []
    bxdata = []
    for dirname in games:
        aname = os.path.join(datadir, dirname)
        game = LoadGame(aname)
        rxdata.append(game.stats[stat][0])
        gxdata.append(game.stats[stat][1])
        bxdata.append(game.stats[stat][2])
        ydata.append(game.players)
    rxdata, ydata = removeOutliers(rxdata, ydata)
    highstat = 0
    total = 0
    highplayers = 0
    for x in rxdata:
        if x >= 150:
            highstat = highstat + 1
        total = total + 1
    for y in ydata:
        if y >= 40:
            highplayers = highplayers + 1
    print("High Player Freq: " + str(highplayers))
    print("Total games: " + str(total))
    print("High Stat Freq: " + str(highstat))

    plot(rxdata, ydata, 'ro')
    xlabel("Red " + stat.capitalize())
    ylabel("Players on Release")
    title("Red " + stat.capitalize() + " vs Players")
    show()      
    #plot(gxdata, ydata, 'go')
    #xlabel("Green " + stat.capitalize())
    #ylabel("Players on Release")
    #title("Green " + stat.capitalize() + " vs Players")
    #show()
    #plot(bxdata, ydata, 'bo')
    #xlabel("Blue " + stat.capitalize())
    #ylabel("Players on Release")
    #title("Blue " + stat.capitalize() + " vs Players")
    #show()
