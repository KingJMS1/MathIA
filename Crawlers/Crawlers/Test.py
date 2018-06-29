from selenium import webdriver
import numpy as np
from scipy import stats

driver = webdriver.Chrome()
driver.get("https://www.youtube.com/playlist?list=PLAquQP_XB6HENbaanPKb6Jy16SaCxY5CM")
elems = driver.find_elements_by_class_name("timestamp")
tostats = []
for e in elems:
    text = e.text
    text = text.split(":")
    toapp = float(text[0]) + (float(text[1])/60)
    tostats.append(toapp)
print(np.mean(tostats))
print(stats.tstd(tostats))
