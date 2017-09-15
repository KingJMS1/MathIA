from . import ImStats
from os import listdir
from bokeh.charts import Histogram, show
from bokeh.layouts import row
import pandas as pd
from scipy import stats


class ImAggregate(object):
    def __init__(self, dirname, filename="data", loadfile=False, verbose=False):
        filename = filename + '.h5'
        self.filename = filename
        self.dirname = dirname
        self.stats = ["means", "rms", "sums", "sum^2s", "variances", "medians", "iqrs", "nuniqcolors", "dimensions",
                      "stddevs", "counts", "names"]
        self.loaded = False
        if loadfile is False:
            self.data = pd.HDFStore(self.dirname + self.filename)
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
            for name in stuff:
                try:
                    if verbose:
                        print("Attempting to add " + name)
                    im = ImStats.ImStats(dirname + name, init=False)
                    means.append(im.stats["mean"])
                    rms.append(im.stats["rms"])
                    sums.append(im.stats["sum"])
                    sum2s.append(im.stats["sum^2"])
                    variances.append(im.stats["variance"])
                    medians.append(im.stats["median"])
                    iqrs.append(im.stats["iqr"])
                    nuniqcolors.append(im.stats["nuniquecolors"])
                    dimensions.append(im.stats["dimensions"])
                    stdDevs.append(im.stats["stdDev"])
                    counts.append(im.stats["count"])
                    names.append(name)
                    try:
                        cols = list('RGBA')
                        iqrcols = list('RGB')
                        self.storeframe("means", pd.DataFrame(means, columns=cols))
                        self.storeframe("rms", pd.DataFrame(rms, columns=cols))
                        self.storeframe("sums", pd.DataFrame(sums, columns=cols))
                        self.storeframe("sum2s", pd.DataFrame(sum2s, columns=cols))
                        self.storeframe("variances", pd.DataFrame(variances, columns=cols))
                        self.storeframe("medians", pd.DataFrame(medians, columns=cols))
                        self.storeframe("iqrs", pd.DataFrame(iqrs, columns=iqrcols))
                        self.storeframe("nuniqcolors", pd.DataFrame(nuniqcolors, columns=["Num Unique Colors"]))
                        self.storeframe("dimensions", pd.DataFrame(dimensions, columns=["Width", "Height"]))
                        self.storeframe("stddevs", pd.DataFrame(stdDevs, columns=cols))
                        self.storeframe("counts", pd.DataFrame(counts, columns=cols))
                        self.data["names"] = pd.DataFrame(names, columns=["Name"])
                    except AssertionError:
                        cols = list('RGB')
                        self.storeframe("means", pd.DataFrame(means, columns=cols))
                        self.storeframe("rms", pd.DataFrame(rms, columns=cols))
                        self.storeframe("sums", pd.DataFrame(sums, columns=cols))
                        self.storeframe("sum2s", pd.DataFrame(sum2s, columns=cols))
                        self.storeframe("variances", pd.DataFrame(variances, columns=cols))
                        self.storeframe("medians", pd.DataFrame(medians, columns=cols))
                        self.storeframe("iqrs", pd.DataFrame(iqrs, columns=cols))
                        self.storeframe("nuniqcolors", pd.DataFrame(nuniqcolors, columns=["Num Unique Colors"]))
                        self.storeframe("dimensions", pd.DataFrame(dimensions, columns=["Width", "Height"]))
                        self.storeframe("stddevs", pd.DataFrame(stdDevs, columns=cols))
                        self.storeframe("counts", pd.DataFrame(counts, columns=cols))
                        self.data["names"] = pd.DataFrame(names, columns=["Name"])
                    if verbose:
                        print("Added " + name + "\n")
                except IOError:
                    print(name + " wasn't a supported image type." + "\n")
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

    def getstat(self, stat):
        if stat not in self.stats:
            raise AssertionError("Not a valid stat")
        if self.loaded is False:
            raise AssertionError("Self not loaded")
        return self.data[stat]