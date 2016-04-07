# encoding:utf-8
import sys
import csv
import time

import urllib2
import cookielib
import base64
import json


def loadUniList(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        unilist = list(reader)
        return unilist
    return []


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

if __name__ == '__main__':
    unilist = loadUniList('list.csv')
    # print unilist[0:2]
    a = unilist[25]
    print a
    print a[0]
    testHttps()


