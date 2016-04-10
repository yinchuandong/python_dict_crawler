# coding:utf-8
import os
import sys
import json
import time

import csv
import re
from uninamecrawler import loadUniList
from eblemcrawler import loadEblemMap 


def checkName():
    unilist, visited = loadUniList('list.csv')
    emap = loadEblemMap('emblem.csv')

    fcsv = open('list_new.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(unilist[0])
    count = 0
    for uni in unilist[1:]:
        if uni[0] not in emap:
            with open('logs_missing_uni.txt', 'a') as flogs:
                flogs.writelines(uni[0] + '\n')
        else:
            extra = emap[uni[0]]
            engname = extra[2]
            nativename = extra[3]
            uni[6] = engname if uni[6] == '' else uni[6]
            uni[7] = nativename if nativename != '' else uni[7]
        writer.writerow(uni)
        count = count + 1
        # break
        # print uni
        # print extra
        # break
    fcsv.close()
    print count
    return


def checkAka():
    unilist, visited = loadUniList('list_check_aka.csv.csv')

    fcsv = open('list_check_aka_new.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(unilist[0])
    count = 0
    for uni in unilist[1:]:
        url = uni[5]
        urlarr = url.split('.')
        if len(urlarr) >= 3:
            aka = urlarr[1].upper()
            uni[-1] = aka if uni[-1] == '' else uni[-1]
        else:
            with open('logs_noaka.txt', 'a') as flogs:
                flogs.writelines(uni[0] + '\n')
        writer.writerow(uni)
        
        print uni
        print extra
        break

    fcsv.close()

    return


def checkNativeName():
    emap2 = loadEblemMap('emblem_2.csv')
    unilist, visited = loadUniList('list_new3.csv')
    count = 0
    total = 0
    fcsv = open('list_check_native_name.csv', 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(unilist[0])
    for i in range(len(unilist[1:])):
        uni = unilist[i]
        # if uni[4] != 'true':
            # continue
        if uni[0] in emap2:
            extra = emap2[uni[0]]

            if uni[6] != '' and uni[7] == '' and extra[3] != '':
                uni[7] = extra[3]
                count = count + 1
                # print uni
        writer.writerow(uni)
        total = total + 1
    print count, total

    fcsv.close()
    return


def checkEmblem():
    unilist, visited = loadUniList('list_check_native_name.csv')
    with open('logs_no_emblem.txt', 'w') as f:
        idx = 0
        for uni in unilist[1:]:
            idx = idx + 1
            if uni[4] != 'true':
                continue
            imgname = uni[2]
            # if not os.path.exists('/Users/yinchuandong/Dropbox/uniname/emblem_v0/' + imgname):
            if not os.path.exists('emblem/' + imgname):
                f.writelines(str(idx) + ',' + uni[0] + ',' + imgname + '\n')
    return


def checkEmblemOfManualUni():
    
    return

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

if __name__ == '__main__':
    # checkName()
    # checkAka()
    # checkNativeName()
    # checkEmblem()


