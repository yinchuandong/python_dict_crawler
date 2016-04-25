# coding:utf-8
import os
import sys
import time

import csv
import cPickle
import re
from bs4 import BeautifulSoup


def loadData(filename):
    li = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        li = list(reader)
    return li


def parser(html):
    doc = BeautifulSoup(html, 'lxml')
    tag_head = doc.select('h1#firstHeading')
    if not tag_head: 
        return
    if 'Search results' in tag_head[0].text:
        return ''
    tag_content = doc.select('div#mw-content-text')
    if not tag_content:
        return
    tag_p = tag_content[0].select('p')[0]
    text = encode(tag_p)

    # for those with bold
    pattern = '\(.*?(<b>.*?<\/b>).*?\)'
    matches = re.search(pattern, text)
    if matches:
        rakas = matches.group(0)
        h = BeautifulSoup(rakas, 'lxml')
        tag_b = h.select('b')
        akalist = [encode(b.text) for b in tag_b]
        return akalist

    pattern = '\(.*?(<i>.*?<\/i>).*?\)'
    matches = re.search(pattern, text)
    if matches:
        rakas = matches.group(0)
        h = BeautifulSoup(rakas, 'lxml')
        tag_b = h.select('i')
        akalist = [encode(b.text) for b in tag_b]
        return akalist

    pattern = '\(.*?\)'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        txt = ''
        key = 'known as'
        for m in matches:
            if len(m) > 30 and  key in m:
                txt = m
                break
        if len(txt) == 0:
            return
        import HTMLParser
        html_parser = HTMLParser.HTMLParser()
        txt = html_parser.unescape(txt.decode('utf-8')).encode('utf-8')
        start = txt.find(key) + len(key) + 1
        txt = txt[start:-1]
        txt = re.split('[,]? or ', txt)
        return txt
    return

def encode(ustr):
    ustr = ustr.encode('utf-8')
    return ustr

def mainParse():
    unilist = loadData('list_0414.csv')
    fcsv = open('list_wiki_aka_3.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(['id', 'uniname', 'aka'])
    
    listWithAka = []    
    for uni in unilist[15:]:
        uniname = uni[1]
        # print uniname
        filename = 'html_wiki_3/' + uniname + '.html'
        if not os.path.exists(filename):
            continue
        with open(filename, 'rb') as f:
            html = f.read()
            akalist = parser(html)
            if akalist:
                akastr = '/'.join(akalist)
                print uniname, '---', akastr
                writer.writerow([uni[0], uniname, akastr])
                listWithAka.append([uni[0], uniname, akalist])
            # print html
        # print uni
        # break
    fcsv.close()
    cPickle.dump(listWithAka, open('list_with_aka_3.pkl', 'wb'))
    return

def mergeAka():
    unilist = loadData('list_0414.csv')
    akalist = cPickle.load(open('list_with_aka_0.pkl', 'rb'))
    akaMap = {}
    for aka in akalist:
        akaMap[aka[0]] = aka
    # print len(akalist)
    fcsv = open('list_0423.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(unilist[0])
    for uni in unilist[1:]:
        id = uni[0]
        if id in akaMap:
            newAka = akaMap[id][-1]
            oldAka = uni[-1].split('/')
            for naka in newAka:
                if naka in oldAka: continue
                # replate UNIMELB with UniMelb
                if naka.upper() in oldAka:
                    k = oldAka.index(naka.upper())
                    oldAka[k] = naka
                else:
                    oldAka.append(naka)
            akastr = '/'.join(oldAka)
            uni[-1] = akastr
            # break
        writer.writerow(uni)
    return

def checkEngname():
    # google translate may add comma, leading aka error
    unilist = loadData('list_0414.csv')
    id = 1 
    length = len(unilist[0])
    for uni in unilist[1:]:
        id = id + 1
        if len(uni) != length:
            print id
    print unilist[168]
    return

def checkEmblem():
    unilist = loadData('list_0423.csv')
    count = 0
    for uni in unilist[1:]:
        # if uni[3] != 'true': continue
        if not os.path.exists('emblem_0413/' + uni[0] + '.png'):
            print uni[0], '---', uni[1]
            count = count + 1
    print count
    return


if __name__ == '__main__':
    # mergeAka()
    # checkEngname()
    # checkEmblem()
    mainParse()