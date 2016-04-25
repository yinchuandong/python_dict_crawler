# coding:utf-8
import os
import sys
import json
import time

import csv
import re
from akaparser import loadData


def checkWebsite():
    import requests
    logs_file = 'logs_website_invalid.csv'
    fcsv = open(logs_file, 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(['id','name', 'error','url', 'finalurl'])
    idx = 1
    unilist = loadData('list_0423.csv')
    for uni in unilist[1:]:
        idx = idx + 1
        url = uni[4]
        if url == '':
            continue
        print url
        try:
            res = requests.get(url, timeout=20)
        except Exception, e:
            print e
            writer.writerow([uni[0], uni[1], 'exception', uni[4], ''])
        else:
            if res.status_code != 200:
                print res.status_code, res.history, res.url
                writer.writerow([uni[0], uni[1], 'badcode:' + str(res.status_code), uni[4], res.url.encode('utf-8')])
            if res.status_code == 200 and res.history:
                print res.status_code, res.history, res.url
                writer.writerow([uni[0], uni[1], 'redirect', uni[4], res.url.encode('utf-8')])
        # break
    return


def loadInvalidWebsite(filename):
    rtList = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        rtList = list(reader)
    return rtList


def mergeWikiWebsite():
    from eblemcrawler import loadEblemMap
    emap = loadEblemMap('emblem_2.csv')
    siteList = loadInvalidWebsite('logs_website_invalid.csv')

    error = 0
    correct = 0
    writer = csv.writer(open('logs_website_merge.csv', 'wb'))
    writer.writerow(siteList[0])
    for site in siteList[1:]:
        if site[2] == 'redirect':
            writer.writerow(site)
            continue
        site[-1] = ''  # remove non redirect url
        name = site[1]
        error = error + 1
        if name in emap:
            url = emap[name][-1]
            if url.startswith('http'):
                correct = correct + 1
                site[-1] = url
        writer.writerow(site)
    print error, correct
    return


def correctWebsite():
    sitelist = []
    with open('logs_website_merge.csv', 'rb') as f:
        reader = csv.reader(f)
        sitelist = list(reader)[1:]
    sitemap = {}
    for s in sitelist:
        sitemap[s[0]] = s

    unilist = loadData('list_0425_2.csv')
    writer = csv.writer(open('list_0425_3.csv', 'wb'))
    writer.writerow(unilist[0])
    count = 0
    for uni in unilist[1:]:
        id = uni[0]
        if id in sitemap and sitemap[id][-1] != '':
            count = count + 1
            uni[4] = sitemap[id][-1]
        writer.writerow(uni)
    print count


def testUtf8Normalization():
    a_list = u'Université de Strasbourg'
    b_em = u'Université de Strasbourg'
    c_wiki = 'Université de Strasbourg'
    print 'a_list', a_list.split()
    print 'b_em', b_em.split()
    print 'c_wiki', c_wiki.split()
    
    filename = a_list + '.test'
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.writelines('hh')

    files = os.listdir('.')
    newname = files[-1]
    print filename.split()
    print newname.split()
    print os.path.exists(filename)
    print os.path.exists(newname)

    from unicodedata import normalize
    a1 = normalize('NFC', unicode(filename))
    b1 = normalize('NFC', newname.decode('utf-8'))
    print a1.encode('utf-8').split()
    print b1.encode('utf-8').split()

    if os.path.exists(filename):
        os.remove(filename)
    return


def translate():
    import goslate
    gs = goslate.Goslate()
    print(gs.translate('hello world', 'de'))
    return

if __name__ == '__main__':
    # checkWebsite()
    # mergeWikiWebsite()
    # correctWebsite()
    translate()