# coding:utf-8
import os
import sys
import csv
import time

import urllib2
import urllib


def loadUniList(filename, savedir='html_wiki'):
    unilist = []
    visited = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        unilist = list(reader)
    files = os.listdir(savedir)
    for filename in files:
        uniname = filename.split('.html')[0]
        visited.append(uniname)
    return unilist, visited


def testHttps():
    import httplib
    url = "en.m.wikipedia.org"
    c = httplib.HTTPSConnection(url)
    c.request("GET", "/w/index.php?search=Universit%C3%A4t+Innsbruck")
    response = c.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    print response.getheader('location')
    return


def testRequest(uniname, keyword, savedir='html_wiki'):
    import requests
    # url = "https://en.m.wikipedia.org/w/index.php?search=Universit%C3%A4t+Innsbruck"
    url = "https://en.wikipedia.org/w/index.php?search=" + keyword
    res = requests.get(url)

    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = uniname + '.html'
    with open(savedir + '/' + filename, 'wb') as fd:
        for chunk in res.iter_content(100):
            fd.write(chunk)
    return

if __name__ == '__main__':
    unilist, visited = loadUniList('list_new3.csv', 'html_wiki_2')
    # a = unilist[25]
    # print a
    # print a[0]
    # print visited
    # testRequest('Universität Innsbruck')
    for uniname in unilist[1:]:
        if uniname[0] in visited:
            continue
        if '/' in uniname[0]:
            continue
        print uniname[0]
        engname = uniname[6]
        if engname == '':
            testRequest(uniname[0], uniname[0], 'html_wiki_2')
        else:
            testRequest(uniname[0], engname, 'html_wiki_2')
        time.sleep(0.5)
