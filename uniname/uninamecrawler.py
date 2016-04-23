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

def crawlEngnameFirst():
    unilist, visited = loadUniList('list_0414.csv', 'html_wiki_3')
    for uni in unilist[1:]:
        uniname = uni[1]
        if uniname in visited:
            continue
        if '/' in uniname:
            continue
        print uniname
        engname = uni[5]
        if engname == '':
            testRequest(uniname, uniname, 'html_wiki_3')
        else:
            testRequest(uniname, engname, 'html_wiki_3')
        time.sleep(0.5)


def crawlUninameFirst():
    unilist, visited = loadUniList('list_0414.csv', 'html_wiki')
    for uni in unilist[1:]:
        uniname = uni[1]
        if uniname in visited:
            continue
        if '/' in uniname:
            continue
        print uniname
        testRequest(uniname, uniname, 'html_wiki')
        time.sleep(0.5)


if __name__ == '__main__':
    # testRequest('Universität Innsbruck')
    # crawlEngnameFirst()
    crawlUninameFirst()
    
