from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import unicodedata
import time

urllist = [
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=1",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=2",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=3",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=4",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=5",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=6",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=7",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=8",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=9",
    "http://store.steampowered.com/search/?sort_by=Released_DESC&tags=4166&page=10",
]


def toname(string):
    name = ''
    for c in string:
        if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ':
            name = name + c
    if name[-1] == ' ':
        name = name[0:-1]
    return name


def doinit(driver):
    driver.get(url)
    imgs = driver.find_elements_by_css_selector('img')
    names = driver.find_elements_by_css_selector('span.title')
    imglinks = [img.get_attribute('src') for img in imgs if 'apps' in img.get_attribute('src')]
    namelist = [e.text for e in names]


driver = webdriver.Chrome()
for url in urllist:
    driver.get(url)
    imgs = driver.find_elements_by_css_selector('img')
    names = driver.find_elements_by_css_selector('span.title')
    imglinks = [img.get_attribute('src') for img in imgs if 'apps' in img.get_attribute('src')]
    namelist = [e.text for e in names]
    # Output

    index = 0
    for e in namelist:
        imglist = []
        name = toname(e)
        try:
            os.mkdir("/data/" + name)
        except FileExistsError:
            pass
        names[index].click()

        if 'agecheck/app' in driver.current_url:
            driver.find_element_by_name("ageYear").click()
            opts = driver.find_elements_by_css_selector('option')
            for e in opts:
                if str(e.get_attribute('value')) == '1990':
                    e.click()
            driver.find_element_by_class_name('btnv6_blue_hoverfade').click()
        elif 'agecheck' in driver.current_url:
            driver.find_element_by_css_selector('a.btn_grey_white_innerfade').click()
            pass

        iduse = driver.current_url.split("/")[4]

        images = driver.find_elements_by_css_selector('a.highlight_screenshot_link')

        for oe in images:
            strn = oe.get_attribute('href')
            imglist.append(strn.split("?url=")[1])
        try:
            os.remove("/data/" + name + "/imagelinks")
        except FileNotFoundError:
            pass
        file = open("/data/" + name + "/imagelinks", 'w+')
        file.write(str(iduse) + "\n")
        file.write(str(len(imglist)) + "\n")
        file.write("\n".join(imglist))
        file.close()
        index = index + 1
        driver.get(url)
        imgs = driver.find_elements_by_css_selector('img')
        names = driver.find_elements_by_css_selector('span.title')
        imglinks = [img.get_attribute('src') for img in imgs if 'apps' in img.get_attribute('src')]
        namelist = [e.text for e in names]
        time.sleep(1)
driver.close()