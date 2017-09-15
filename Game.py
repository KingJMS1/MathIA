import os
import scipy
import numpy as np
from ImageStatistics import UsefulImDirectory
import scipy as sp
import ast
from bokeh.charts import Histogram, show
import pandas as pd

class Game(object):
    def __init__(self, gamefolder):
        self.gamefolder = os.path.abspath(gamefolder)
        file = open(os.path.join(gamefolder, "sales"))
        self.releaseplayers = int(file.readline().rstrip("\n").split(": ")[1])
        file.close()
        file = open(os.path.join(gamefolder, "imagelinks"))
        self.gameid = int(file.readline().rstrip("\n"))
        file.close()
        self.images = UsefulImDirectory.ImAggregate(os.path.join(gamefolder, "imgs"))
        self.stats = ["means", "variances", "medians", "iqrs", "stddevs", "contrast"]
        self.data = None
        
    def getdata(self):
        if self.data is None:
            self.data = [self.images.getdata("reds"), self.images.getdata("greens"), self.images.getdata("blues")]
            return self.data
        else:
            return self.data
    
    def getcontrast(self):
        return self.images.getdata("contrast")
    
    def getplayers(self):
        return self.releaseplayers
    
    def calcstat(self, stat):
        if stat not in self.stats:
            raise AssertionError("Please choose a valid stat")
        if stat == "means":
            return [np.mean(x) for x in self.getdata()]
        elif stat == "variances":
            return [np.var(x) for x in self.getdata()]
        elif stat == "medians":
            return [np.median(x) for x in self.getdata()]
        elif stat == "iqrs":
            return [sp.stats.iqr(x) for x in self.getdata()]
        elif stat == "stddevs":
            return [np.std(x) for x in self.getdata()]
        elif stat == "contrast":
            return self.getcontrast()
            
        
    def storestats(self):
        file = open(os.path.join(self.gamefolder, "stats"), 'w+')
        for x in self.stats:
            towrite = self.calcstat(x)
            file.write(x + ": " + str(towrite) + "\n")
        file.close()
        
    def readstats(self):
        file = open(os.path.join(self.gamefolder, "stats"))
        means = ast.literal_eval(file.readline().rstrip("\n").split(": ")[1])
        variances = ast.literal_eval(file.readline().rstrip("\n").split(": ")[1])
        medians = ast.literal_eval(file.readline().rstrip("\n").split(": ")[1])
        iqrs = ast.literal_eval(file.readline().rstrip("\n").split(": ")[1])
        stddevs = ast.literal_eval(file.readline().rstrip("\n").split(": ")[1])
        line = file.readline().rstrip("\n").split(": ")[1]
        try:
            contrast = ast.literal_eval(line)
        except ValueError:
            tocont = line.replace("nan, ", "")
            contrast = ast.literal_eval(tocont)
        file.close()
        return {"means": means, "variances": variances, "medians": medians, "iqrs": iqrs, "stddevs": stddevs, "contrast": contrast}

    def colorhistogram(self, color):
        colors = ["red", "green", "blue"]
        if color.lower() not in colors:
            raise AssertionError("Please pick a valid color")
        self.histograms = {}
        tohist = {"red": 0, "green": 1, "blue": 2}
        self.histograms[color.lower()] = Histogram(pd.DataFrame(self.getdata()[tohist[color.lower()]], columns=[color.lower()]),values=color.lower(),color=color.capitalize(),bins=255)
        show(self.histograms[color.lower()])