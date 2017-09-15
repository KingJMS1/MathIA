from . import SimplifiedImStats
from os import listdir
from bokeh.charts import Histogram, show
from bokeh.layouts import row
import pandas as pd
from scipy import stats
import numpy as np
import scipy as sp
import os

class ImAggregate(object):  # Computes simple statistics the correct way.
    def __init__(self, dirname, filename="data", loadfile=False, verbose=False):
        filename = filename + '.h5'
        self.filename = filename
        self.dirname = dirname
        self.stats = ["means", "variances", "medians", "iqrs", "stddevs"]
        self.loaded = False
        if loadfile is False:
            self.data = {}
            stuff = listdir(dirname)
            self.loaded = True
            means = []
            rms = []
            sums = []
            sum2s = []
            variances = []
            medians = []
            iqrs = []
            nuniqcolors = []
            dimensions = []
            stdDevs = []
            counts = []
            names = []
            reds = []
            greens = []
            blues = []       
            contrast = []
            for name in stuff:
                try:
                    if verbose:
                        print("Attempting to add " + name)
                    im = SimplifiedImStats.ImStats(os.path.join(dirname, name), init=False)
                    reds = reds + im.reds
                    greens = greens + im.greens
                    blues = blues + im.blues
                    contrast.append(im.contrast)
                    if verbose:
                        print("Added " + name + "\n")
                except IOError:
                    print(name + " wasn't a supported image type." + "\n")
            self.data["reds"] = reds
            self.data["blues"] = blues
            self.data["greens"] = greens
            self.data["contrast"] = contrast
            print("Done adding " + dirname + "\n")
        elif loadfile is True:
            self.load()

    def load(self):
        if self.loaded:
            raise AssertionError("Already loaded.")
        self.data = pd.HDFStore(self.dirname + self.filename)
        self.loaded = True

    def histograms(self, stat, verbose=False):
        if stat not in self.stats and stat is not "names":
            print("Please choose a valid statistic.\n")
        elif stat not in ["nuniqcolors", "dimensions"]:
            data = self.data[stat]
            rhist = Histogram(data, values='R',  color='Red', title="Red " + stat[0].upper() + stat[1:])
            ghist = Histogram(data, values='G', color='Green', title="Green " + stat[0].upper() + stat[1:])
            bhist = Histogram(data, values='B', color='Blue', title="Blue " + stat[0].upper() + stat[1:])
            if verbose:
                print(data)
            show(row(rhist, ghist, bhist))
        elif stat == "nuniqcolors": 
            data = self.data[stat]
            hist = Histogram(data, values="Num Unique Colors", color='Purple', title="Number of Unique Colors")
            if verbose:
                print(data)
            show(hist)
        elif stat == "dimensions":
            data = self.data[stat]
            whist = Histogram(data, values="Width", color="Purple", title="Width Histogram")
            hhist = Histogram(data, values="Height", color='Purple', title="Height Histogram")
            if verbose:
                print(data)
            show(row(whist, hhist))

    def storeframe(self, stat, dataframe):
        self.data[stat] = dataframe

    def getdata(self, data):
        return self.data[data]
    
    def getstat(self, stat):
        if stat not in self.stats:
            raise AssertionError("Please pick a valid stat")
        if stat == "means":
            redmean = np.mean(self.data["reds"])
            greenmean = np.mean(self.data["greens"])
            bluemean = np.mean(self.data["blues"])
            return (redmean, greenmean, bluemean)
        if stat == "variances":
            redvar = np.std(self.data["reds"])**2
            greenvar = np.std(self.data["greens"])**2
            bluevar = np.std(self.data["blues"])**2
            return (redvar, greenvar, bluevar)
        if stat == "medians":
            redmed = sp.median(self.data["reds"])
            greenmed = sp.median(self.data["greens"])
            bluemed = sp.median(self.data["blues"])
            return (redmed, greenmed, bluemed)
        if stat == "iqrs":
            rediqr = stats.iqr(self.data["reds"])
            greeniqr = stats.iqr(self.data["greens"])
            blueiqr = stats.iqr(self.data["blues"])
            return (rediqr, greeniqr, blueiqr)
        if stat == "stddevs":
            redstd = np.std(self.data["reds"])
            greenstd = np.std(self.data["greens"])
            bluestd = np.std(self.data["blues"])
            return (redstd, greenstd, bluestd)            