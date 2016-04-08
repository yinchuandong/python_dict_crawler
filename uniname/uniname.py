# coding:utf-8
import os
import sys
import csv
import time

import urllib2
import urllib


def loadUniList(filename):
    unilist = []
    visited = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        unilist = list(reader)
    files = os.listdir('html_wiki/')
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


def testRequest(uniname):
    import requests
    # url = "https://en.m.wikipedia.org/w/index.php?search=Universit%C3%A4t+Innsbruck"
    url = "https://en.m.wikipedia.org/w/index.php?search=" + uniname
    res = requests.get(url)

    if not os.path.exists('html_wiki'):
        os.makedirs('html_wiki')
    filename = uniname + '.html'
    with open('html_wiki/' + filename, 'wb') as fd:
        for chunk in res.iter_content(100):
            fd.write(chunk)
    return

if __name__ == '__main__':
    unilist, visited = loadUniList('list.csv')
    # a = unilist[25]
    # print a
    # print a[0]
    # print visited
    # testRequest('Universität Innsbruck')
    # for uniname in unilist[1:]:
    #     if uniname[0] in visited:
    #         continue
    #     if '/' in uniname[0]:
    #         continue
    #     print uniname[0]
    #     testRequest(uniname[0])
    #     time.sleep(0.5)
