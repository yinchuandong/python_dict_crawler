# coding:utf-8

import os
import sys
import json

import csv
from bs4 import BeautifulSoup
from uninamecrawler import loadUniList
from unicodedata import normalize

def main():
    savedir = 'html_wiki_2'
    files = os.listdir(savedir)
    # files = [
    #     "Tsinghua University.html",
    #     "Abu Dhabi University.html",
    #     "American University in Dubai.html",
    #     "Tokyo University.html",
    #     ]
    # print len(files)
    if os.path.exists('logs_invalidfile.txt'):
        os.remove('logs_invalidfile.txt')
    header = ["filename", "emblem", "engname", "nickname", "website"]
    fcsv = open('emblem_2.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(header)
    for i in range(len(files)):
        # very important, otherwise even if the string are the same,
        # it will be differently treated
        filename = normalize('NFC', files[i].decode('utf-8')).encode('utf-8')
        print i, filename
        with open(savedir + '/' + filename) as f:
            html = f.read()
            # filename, emblem, engname, nickname, website = parse(files[i], html)
            uni = parse(filename, html)
            # print uni
            if uni:
                writer.writerow(uni)
        # break 

    fcsv.close()
    return


def parse(filename, html):
    doc = BeautifulSoup(html, 'lxml')
    # print doc.title
    table = doc.select('table.vcard')
    if len(table) == 0:
        invalidfile = open('logs_invalidfile.txt', 'a')
        invalidfile.writelines(filename + '\n')
        invalidfile.close()
        return None

    tag_nickname = table[0].select('span.nickname')
    nickname = tag_nickname[0].text.encode('utf-8') if tag_nickname else ''
    # print nickname

    # tag_engname = table[0].select('caption')
    # engname = tag_engname[0].text.encode('utf-8') if tag_engname else ''
    # print engname
    tag_engname = doc.select('h1#firstHeading')
    engname = tag_engname[0].text.encode('utf-8') if tag_engname else ''

    tag_emblem = table[0].select('a.image img')
    emblem = tag_emblem[0]['src'].encode('utf-8') if tag_emblem else ''
    # print emblem

    tag_website = table[0].select('a.external')
    website = tag_website[0]['href'].encode('utf-8') if tag_website else ''
    # print (website)
    uniname = filename.split('.html')[0]
    return (uniname, emblem, engname, nickname, website)


def test():
    filename = 'Inner Mongolia Polytechnic University.html'
    with open('html_wiki_2/' + filename, 'r') as f:
        html = f.read()
        rt = parse(filename, html)
        print rt
    return


if __name__ == '__main__':
    # main()
    test()