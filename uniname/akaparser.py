# coding:utf-8
import os
import sys
import time

import csv
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
        return ''
    if 'Search results' in tag_head[0].text:
        return ''
    tag_content = doc.select('div#mw-content-text')
    if not tag_content:
        return ''
    tag_p = tag_content[0].select('p')[0]
    text = encode(tag_p)

    # for those with bold
    pattern = '\(.*?(<b>.*?<\/b>).*?\)'
    matches = re.search(pattern, text)
    if matches:
        rakas = matches.group(0)
        h = BeautifulSoup(rakas, 'lxml')
        # print h.select('b')
        return

    pattern = '\(.*?(<i>.*?<\/i>).*?\)'
    matches = re.search(pattern, text)
    if matches:
        rakas = matches.group(0)
        h = BeautifulSoup(rakas, 'lxml')
        # print h.select('i')
        return

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
        print txt
        import HTMLParser
        html_parser = HTMLParser.HTMLParser()
        txt = html_parser.unescape(txt.decode('utf-8')).encode('utf-8')
        start = txt.find(key) + len(key) + 1
        txt = txt[start:-1]
        txt = re.split('[,]? or ', txt)
        print txt
        # print text
    # print text
    return

def encode(ustr):
    ustr = ustr.encode('utf-8')
    return ustr

def main():
    unilist = loadData('list_0414.csv')
    for uni in unilist[1:10]:
        uniname = uni[1]
        filename = 'html_wiki_2/' + uniname + '.html'
        if not os.path.exists(filename):
            continue
        with open(filename, 'rb') as f:
            html = f.read()
            parser(html)
            # print html
        # print uni
        break
    return

if __name__ == '__main__':
    main()