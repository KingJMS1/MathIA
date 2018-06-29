from CrawlerFramework.Downloader import Downloader
import os

# For ease of rememberance
datapath = os.path.abspath("/mnt/d/data/")  # Linux subsystem for Windows is useful.
todownload = os.listdir(datapath)
todownload.remove("FakeGames")
fakelist = os.path.join(datapath, "FakeGames")


# Remove games without sales statistics
fakegame = "NotYet"
file = open(fakelist)
while(fakegame != ""):
    fakegame = file.readline().rstrip("\n")
    if fakegame != "":
        todownload.remove(fakegame)
# ToDownload is now ready to actually download with

# Uses downloader class to download, class takes the "imagelinks" filelocation
for game in todownload:
    path = os.path.join(datapath, game, "imagelinks")
    downer = Downloader(path)
    downer.download()