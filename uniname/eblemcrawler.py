# coding:utf-8
import os
import sys
import json
import time

import csv
from bs4 import BeautifulSoup
from uninamecrawler import loadUniList
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

def main():
    unilist, visited = loadUniList('list_check_native_name.csv')
    unilist = unilist[1:]
    emap = loadEblemMap('emblem_2.csv')
    # print emap['Central South University']
    # print emap['Charité - Universitätsmedizin Berlin']
    if os.path.exists('logs_crawler_emblem.txt'):
        os.remove('logs_crawler_emblem.txt')
    count = 0
    for uni in unilist:
        if uni[0] not in emap:
            continue
        count = count + 1
        print count
        emblem = emap[uni[0]]
        url = emblem[1]
        if len(url) == 0:
            continue
        savename = uni[2]
        if os.path.exists('emblem/' + savename):
            continue
        print uni
        print savename
        print url
        print ''
        try:
            download(savename, 'https:' + url)
        except Exception, e:
            with open('logs_crawler_emblem.txt', 'a') as f:
                f.writelines(savename + '\n')
        time.sleep(0.5)
        # break
    print count
    return

if __name__ == '__main__':
    main()



