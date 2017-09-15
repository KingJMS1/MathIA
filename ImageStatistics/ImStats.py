from PIL import Image, ImageStat
import numpy as np
from scipy import stats
import scipy as sp
import pandas as pd
from bokeh.charts import Histogram, show
from bokeh.layouts import row
import matplotlib.pyplot as plt
import matplotlib.colors as matcolors


class ImStats(object):  # The class of the clunk
    def __init__(self, filename, init=True, verbose=False):
        self.clists = None
        self.image = Image.open(filename)
        if verbose:
            print("Opened")
        if init:                                    # Init is used to decrease the runtime of creating an instance of
            self.image.load()                       # this class by a significant amount. If you don't want to do
        self.wdh, self.hgh = self.image.size        # anything fancy, use init=False.
        if verbose:
            print("Size")
        self.sstats = ImageStat.Stat(self.image)  # extrema, count, sum, sum2, mean, median, rms, var, stddev
        if verbose:
            print("BaseStats")

        self.colors = self.image.getcolors(self.wdh * self.hgh)
        if verbose:
            print("Got colors")
        self.frqlst, self.colorsarray = self.colors_for_array()
        if verbose:
            print("Did colorsforarray")
        self.nuniqcolors = len(self.frqlst)
        if verbose:
            print("Got unique colors")
        self.data = pd.DataFrame(self.colorsarray, index=np.arange(self.nuniqcolors),
                                 columns=['Frq', 'R', 'G', 'B'])
        self.data_frq_indexed = pd.DataFrame(
            np.array(self.colors_for_arrayfrqindex()[1]), index=self.colors_for_arrayfrqindex()[0],
            columns=list('RGB')
        )
        self.data_nofrq = pd.DataFrame(
            np.array(self.colors_for_arraynofrq()[1]), index=range(self.colors_for_arraynofrq()[0]),
            columns=list('RGB')
        )
        self.clists = self.getColorLists()
        self.reds = np.array(self.clists[0])
        self.greens = np.array(self.clists[1])
        self.blues = np.array(self.clists[2])
        if self.clists is None:
            self.clists = self.getColorLists()
        if verbose:
            print("Got colorlists")
        if init:
            self.redsorted = np.array(sorted(self.clists[0]))
            self.greensorted = np.array(sorted(self.clists[1]))
            self.bluesorted = np.array(sorted(self.clists[2]))
            if verbose:
                print("Arrays from clists")

        self.RedHist = None  # Easiest representation
        self.GreenHist = None
        self.BlueHist = None

        self.colorPlot = None  # Represents all of the data, very bad for performance

        self.stats = {"extrema": self.sstats.extrema, "count": self.sstats.count, "sum": self.sstats.sum,
                      "sum^2": self.sstats.sum2, "mean": self.sstats.mean, "median": self.sstats.median,
                      "rms": self.sstats.rms, "variance": self.sstats.var, "stdDev": self.sstats.stddev,
                      "nuniquecolors": self.nuniqcolors, "iqr": self.getIQR(), "dimensions": [self.wdh, self.hgh]}
        if verbose:
            print("Got final stats")

    def colors_for_array(self):
        gcolors = self.colors
        runner = []
        frqs = []
        for tple in gcolors:
            daint = tple[0]
            datup = tple[1]
            frqs.append(daint)
            runner.append([daint, datup[0], datup[1], datup[2]])
        return frqs, np.array(runner)

    def getIQR(self):
        return [sp.stats.iqr(self.clists[0]), sp.stats.iqr(self.clists[1]), sp.stats.iqr(self.clists[2])]

    def colors_for_arraynofrq(self):
        gcolors = self.colors
        runner = []
        frqs = []
        num = 0
        nfq = None
        for tple in gcolors:
            list_inside = []
            daint = tple[0]
            datup = tple[1]
            frqs.append(daint)
            nfq = daint
            num += daint
            list_inside.append(datup[0])
            list_inside.append(datup[1])
            list_inside.append(datup[2])
            for i in range(nfq):
                runner.append(list_inside)
        return num, np.array(runner)

    def colors_for_arrayfrqindex(self):
        gcolors = self.colors
        runner = []
        frqs = []
        for tple in gcolors:
            list_inside = []
            datup = tple[1]
            frqs.append(tple[0])
            list_inside.append(datup[0])
            list_inside.append(datup[1])
            list_inside.append(datup[2])
            runner.append(list_inside)
        return frqs, np.array(runner)

    def colorstoplot(self, cutoff=0):
        gcolors = self.colors
        frqs = []
        x = []
        y = []
        z = []
        switch = False
        for tple in gcolors:
            for e in tple:
                if type(e) == int and e <= cutoff:
                    switch = True
                elif type(e) == int:
                    frqs.append(e)
                elif type(e) == tuple and switch is False:
                    x.append(e[0])
                    y.append(e[1])
                    z.append(e[2])
                else:
                    switch = False
        return x, y, z, frqs

    def convcolors(self):
        """Returns colors without the 4th channel, if you aren't using it.
        """
        gcolors = self.colors
        runner = []
        for tple in gcolors:
            runner.append(tple[0])
            runner.append(tple[1][0:3])
        return runner

    def basecolors(self):
        wdh, hgh = self.image.size
        return self.image.getcolors(wdh * hgh)

    def outcolors(self):
        """Outputs the colors with space delimiters, suitable for excel, to some degree."""
        toconv = str(self.convcolors())
        end = ''
        nlinprv = False
        end = end + "FRQ R G B \n"
        for c in toconv:
            if c == ',' and nlinprv is False:
                end = end + ' '
            elif c == ',' and nlinprv is True:
                nlinprv = False
            elif c == ')':
                end = end + '\n'
                nlinprv = True
            elif c == '[' or c == ']' or c == '(' or c == ' ':
                nlinprv = False
            else:
                end = end + c
                nlinprv = False
        end = end + "Be sure to use space delimiters."
        return end

    def show(self):
        self.image.show()

    def createhistograms(self):
        self.RedHist = Histogram(self.data_nofrq, values='R', color='Red', bins=255)
        self.GreenHist = Histogram(self.data_nofrq, values='G', color='Green', bins=255)
        self.BlueHist = Histogram(self.data_nofrq, values='B', color='Blue', bins=255)

    def displayhistograms(self):
        """Displays histograms and creates them if the red histogram does not exist."""
        if self.RedHist is None:
            print("The histograms don't exist, so they will be created")
            self.createhistograms()
        show(row(self.RedHist, self.GreenHist, self.BlueHist))

    def displayColorPlot(self, cutoff=0):  # 4-Dimensional scatter plot (4th dimension is color, log scale)
        """Displays a 4-dimensional scatter plot of the colors in your image. 4th dimension is frequency represented
        by color.
        cutoff: int, prevents colors with frequencies below or equal to it from appearing.
        """
        figure = plt.figure()
        axes = figure.add_subplot(111, projection='3d')
        xs, ys, zs, frqs = self.colorstoplot(cutoff)
        scp = axes.scatter(xs, ys, zs, c=frqs, norm=matcolors.LogNorm(), cmap=plt.cm.get_cmap('viridis'))
        plt.colorbar(scp)
        plt.show()

    def getColorLists(self):
        if self.clists is not None:
            return self.clists
        gcolors = self.colors
        red = []
        green = []
        blue = []
        for tple in gcolors:
            daint = tple[0]
            datup = tple[1]
            for oe in range(daint):
                red.append(datup[0])
                green.append(datup[1])
                blue.append(datup[2])
        return red, green, blue
