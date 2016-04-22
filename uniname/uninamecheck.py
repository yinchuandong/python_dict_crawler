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
    from shutil import copyfile
    unilist, visited = loadUniList('list_check_aka.csv')
    dst_dir = 'emblem_true/'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    count = 0
    for uni in unilist[1:]:
        count = count + 1
        if uni[4] == 'true' and os.path.exists('emblem/' + uni[2]):
            copyfile('emblem/' + uni[2], dst_dir + uni[2])

    return


def checkWebsite():
    import requests
    logs_file = 'logs_invalid_website.txt'
    if os.path.exists(logs_file):
        os.remove(logs_file)
    unilist, visited = loadUniList('list_check_aka.csv')
    idx = 1
    for uni in unilist[1:]:
        idx = idx + 1
        url = uni[5]
        if url == '':
            continue
        print url
        # url = 'https://en.wikipedia.org/w/index.php?search=Peking University'
        try:
            res = requests.get(url)
        except Exception, e:
            print e
            with open(logs_file, 'a') as f:
                f.writelines(str(idx) + ',' + uni[0] + ',' + uni[4] + '\n')
        else:
            if res.status_code != 200 or res.history:
                print res.status_code, res.history, res.url
                with open(logs_file, 'a') as f:
                    f.writelines(str(idx) + ',' + uni[0] + ',' + uni[4] + '\n')
        # break
    return


def checkWebsiteWithError():
    import requests
    logs_file = 'logs_redirect_website.csv'
    fcsv = open(logs_file, 'wb')
    writer = csv.writer(fcsv)
    writer.writerow(['id', 'uniname', 'manual', 'src', 'dst'])

    unilist, visited = loadUniList('list_check_aka.csv')
    errorList = []
    with open('logs_invalid_website2.txt', 'r') as f:
        for line in f.readlines():
            errorList.append(int(line.split(',')[0]))
    # print errorList[0:4]
    idx = 1
    for uni in unilist[1:]:
        idx = idx + 1
        if idx not in errorList:
            continue
        url = uni[5]
        # print url
        try:
            res = requests.get(url)
        except Exception, e:
            print e
            print ''
            li = [str(idx), uni[0], uni[4], url, 'false']
            writer.writerow(li)
        else:
            if res.status_code != 200:
                li = [str(idx), uni[0], uni[4], url, int(res.status_code)]
                writer.writerow(li)

            if res.status_code == 200 and res.history:
                print res.status_code, res.history
                print url, res.url
                print ''
                li = [str(idx), uni[0], uni[4], url, res.url.encode('utf-8')]
                writer.writerow(li)
        # break
    fcsv.close()
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
    # checkEmblemOfManualUni()
    # checkWebsite()
    checkWebsiteWithError()

