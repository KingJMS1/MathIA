import os   
from pylab import *
import numpy as np
from ImageStatistics import ImStats
from ImageStatistics import UsefulImDirectory
import bokeh
from Game import Game


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
    path = os.path.join(datadir, game)
    try:
        legame = Game(path)
        legame.storestats()
    except IndexError:
        file = open(os.path.join(path, "NEP"), 'w+')
        file.close()
        print(game + " did not have enough players")