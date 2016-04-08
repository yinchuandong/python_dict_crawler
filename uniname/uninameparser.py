#encoding:utf-8

import os
import sys
import json

from bs4 import BeautifulSoup

def main():
    files = os.listdir('html_wiki/')
    print len(files)
    for i in range(len(files)):
        with open('html_wiki/' + files[i]) as f:
            html = f.read()
            parse(files[i], html)
        break
    return

def parse(filename, html):
    doc = BeautifulSoup(html, 'lxml')
    print doc.title
    return

if __name__ == '__main__':
    main()