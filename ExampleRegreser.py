import os   
from pylab import *
import numpy as np
import bokeh
from sklearn import linear_model
from LoadGame import LoadGame
import pandas as pd

datadir = os.path.abspath("C:/Users/Owner/Desktop/3d Animations/Images/Abstract/IM STAT EXAMPLES/")
games = os.listdir(datadir)
xdata = []
ydata = []
print(games)
stat = "iqrs"
regression = linear_model.LinearRegression(fit_intercept=True)

if stat == "contrast":
    for dirname in games:
        aname = os.path.join(datadir, dirname)
        print(aname)
        game = LoadGame(aname)
        xdata.append(np.median(game.stats["contrast"]))
        ydata.append(game.players)
    xs = pd.DataFrame(xdata, columns=["Contrast"])
    ys = pd.DataFrame(ydata, columns=["Players"])
    regression.fit(xs, ys["Players"])
    plot(xdata, ydata, 'ko')
    
    print("Coefficient: " + str(regression.coef_))
    print("Interecept: " + str(regression.intercept_))
    print("R^2: " + str(regression.score(xs, ys["Players"])))
    xlabel("Contrast")
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
    plot(rxdata, ydata, 'ro')
    title("Red " + stat.capitalize() + " vs Players")
    xlabel("Red " + stat.capitalize())
    ylabel("Players on Release")
    show()
    plot(gxdata, ydata, 'go')
    xlabel("Green " + stat.capitalize())
    ylabel("Players on Release")
    title("Green " + stat.capitalize() + " vs Players")
    show()
    plot(bxdata, ydata, 'bo')
    xlabel("Blue " + stat.capitalize())
    ylabel("Players on Release")
    title("Blue " + stat.capitalize() + " vs Players")
    show()
