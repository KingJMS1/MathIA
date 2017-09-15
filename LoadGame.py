import os
from Game import Game

class LoadGame(Game):
    def __init__(self, gamefolder):
        self.gamefolder = os.path.abspath(gamefolder)
        file = open(os.path.join(gamefolder, "sales"))
        self.releaseplayers = int(file.readline().rstrip("\n").split(": ")[1])
        file.close()
        file = open(os.path.join(gamefolder, "imagelinks"))
        self.gameid = int(file.readline().rstrip("\n"))
        file.close()
        self.stats = self.readstats()
        self.players = self.releaseplayers