from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os
import unicodedata
import time as sleeper
from datetime import *

months = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}


def fileoverwrite(filename):
    nfile = open(filename, 'w+')
    return nfile

driver = webdriver.Chrome()
namelist = os.listdir("/data/")
try:
    namelist.remove('FakeGames')
except ValueError:
    pass

for name in namelist:
    folder = "/data/" + name + "/"
    file = open("/data/" + name + "/imagelinks")        # Steam ID num is in 1st line for my convenience.
    id = file.readline().rstrip("\n")
    driver.get("https://steamdb.info/app/" + str(id) + "/graphs/")
    pageshouldbe = "https://steamdb.info/app/" + str(id) + "/graphs/"
    pageor = "http://steamdb.info/app/" + str(id) + "/graphs/"
    if driver.current_url not in [pageshouldbe, pageor]:    # Tests if the /graphs/ page exists
        file.close()
        file = fileoverwrite(folder + "sales")
        file.write("Not a game")
        file.close()
        file = open("/data/FakeGames", "a+")                # If it doesn't, usually the item is actually DLC
        file.write(name + "\n")
        file.close()
    else:
        sleeper.sleep(2)
        try:
            chartnum = int(driver.find_element_by_id("js-chart-year").get_attribute("data-highcharts-chart"))
            data = driver.execute_script("return Highcharts.charts[" + str(chartnum) + "].series[0].yData")
            elems = driver.find_elements_by_css_selector("td")  # Gets data and release date
            for ne in elems[2:25]:
                ae = ne.text
                e = ae.split(" ")
                try:
                    if e[0] in months.keys() and int(e[1].strip(",")) in range(1,33) and int(e[2]) in range(1900,2100):
                        rdate = e
                        break
                except IndexError:
                    pass
            rdate = rdate[0:3]                      # Release date
            month = months[rdate[0]]
            day = int(rdate[1].strip(","))
            year = int(rdate[2])
            nrdate = datetime(year, month, day)

            delta = datetime.today() - nrdate       # Uses datetime magic to make my job easier
            negindex = delta.days                   # Number of days before today release was
            try:
                playersonrelease = data[-negindex]  # Finds release day and writes number of players on it
                file = fileoverwrite(folder + "sales")
                file.write("Players on Release: " + str(playersonrelease) + "\n" + str(data))
                file.close()
            except IndexError:
                file = fileoverwrite(folder + "sales")
                file.write("Not enough players")
                file.close()
        except TypeError:
            print("Rejected " + str(name))
            print("Please reopen program and delete all previously acquired games from namelist")
            sleeper.sleep(100)
driver.close()