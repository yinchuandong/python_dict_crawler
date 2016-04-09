# coding:utf-8
import os
import sys
import json
import time

import csv
from bs4 import BeautifulSoup
from uniname import loadUniList
import requests


def loadEblemMap(filename):
    emblemList = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        emblemList = list(reader)[1:]
    emap = {}
    for em in emblemList:
        emap[em[0]] = em
    return emap


def download(savename, url):
    if not os.path.exists('emblem/'):
        os.mkdir('emblem')
    # url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/The_Logo_of_National_Tsing_Hua_University.svg/180px-The_Logo_of_National_Tsing_Hua_University.svg.png"
    res = requests.get(url)
    from PIL import Image
    from StringIO import StringIO
    img = Image.open(StringIO(res.content))
    img.save('emblem/' + savename)
    return

if __name__ == '__main__':
    # download()
    unilist, visited = loadUniList('list.csv')
    unilist = unilist[1:]
    emap = loadEblemMap('emblem.csv')
    # print emap['Central South University']
    # print emap['Charité - Universitätsmedizin Berlin']
    count = 0
    for uni in unilist:
        if uni[0] not in emap:
            continue
        count = count + 1
        emblem = emap[uni[0]]
        url = emblem[1]
        if len(url) == 0:
            continue
        savename = uni[2]
        download(savename, 'https:' + url)
        time.sleep(0.5)
        # break
    print count



