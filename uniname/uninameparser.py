# coding:utf-8

import os
import sys
import json

from bs4 import BeautifulSoup
from uniname import loadUniList

def main():
    # files = os.listdir('html_wiki/')
    files = [
        "Tsinghua University.html",
        # "Abu Dhabi University.html",
        "American University in Dubai.html",
        # "Tokyo University.html",
        ]
    # print len(files)
    for i in range(len(files)):
        with open('html_wiki/' + files[i]) as f:
            html = f.read()
            parse(files[i], html)
        break
    return


def parse(filename, html):
    doc = BeautifulSoup(html, 'lxml')
    # print doc.title
    table = doc.select('table.vcard')
    if len(table) == 0:
        invalidfile = open('invalidfile.txt', 'a')
        invalidfile.writelines(filename + '\n')
        invalidfile.close()
        return

    tag_nickname = table[0].select('span.nickname')
    nickname = tag_nickname[0].text.encode('utf-8') if tag_nickname else ''
    print nickname

    tag_engname = table[0].select('caption')
    engname = tag_engname[0].text if tag_engname else ''
    print engname

    tag_emblem = table[0].select('a.image img')
    emblem = tag_emblem[0]['src'] if tag_emblem else ''
    print emblem

    tag_website = table[0].select('a.external')
    website = tag_website[0]['href'] if tag_website else ''
    print (website)
    return

if __name__ == '__main__':
    main()