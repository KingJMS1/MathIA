import subprocess
import os

# Works on linux
class Downloader(object):
    def __init__(self, fileloc):
        self.loc = os.path.dirname(fileloc)
        file = open(os.path.abspath(fileloc))
        self.downlist = []
        file.readline()
        numimgs = int(file.readline().rstrip("\n"))
        for n in range(numimgs):
            self.downlist.append(file.readline().rstrip("\n"))
        file.close()
    
    def download(self):
        imgloc = os.path.join(self.loc, "imgs")
        try:
            os.mkdir(imgloc)
        except FileExistsError:
            pass
        filenum = 0
        for todown in self.downlist:
            filenum += 1
            subprocess.call(["wget -O " + '"' + os.path.join(imgloc, "img" + str(filenum) + ".png") + '" ' + todown], shell=True)   # Causing security hazards can be fun.