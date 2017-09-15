import os   
from pylab import *
import numpy as np
from ImageStatistics import ImStats
from ImageStatistics import UsefulImDirectory
import bokeh
from Game import Game


datadir = os.path.abspath("C:/Users/Owner/Desktop/3d Animations/Images/Abstract/IM STAT EXAMPLES/")
games = os.listdir(datadir)

for game in games:
    path = os.path.join(datadir, game)
    try:
        legame = Game(path)
        legame.storestats()
    except IndexError:
        file = open(os.path.join(path, "NEP"), 'w+')
        file.close()
        print(game + " did not have enough players")