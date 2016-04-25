# coding:utf-8
import os
import sys
import json
import time

import base64
import hashlib
import re
import csv
from bs4 import BeautifulSoup

def test():
    # filename = 'html_google/Universidad Torcuato di Tella.html'
    # filename = 'html_google/Universidad Nacional de Cordoba.html'
    filename = 'html_google/56ea56a7820e343600f41267.html'
    text = open(filename, 'r').read()
    arr = text.split('/*""*/')
    # print len(arr)
    # search = 'iSGMObiLFSEZStR7HqX3mNKmqmW8iPjzgoQpv9DNY46Njd9o4d6NqMqAoJ'
    # for i in range(len(arr)):
    #     tstr = arr[i]
    #     if search in tstr:
    #         print i
    obj = json.loads(arr[9])
    # with open('google_test.html', 'w') as f:
    #     f.writelines(obj['d'])
    html = obj['d']
    prefix = 'data:image/png;base64,'
    pattern = 'data:image/png;base64,(.*?);'
    matches = re.findall(pattern, html, re.DOTALL)
    print len(matches), '----'
    for m in matches:
        print len(m)

    with open('google_test_2.html', 'w') as f:
        f.writelines(prefix + matches[0].decode('utf-8'))
    return


def oldParse():
    files = os.listdir('html_google/')
    count = 0
    for filename in files:
        text = open('html_google/' + filename, 'r').read()
        arr = text.split('/*""*/')
        if len(arr) < 12: continue
        # print len(arr), filename
        obj = json.loads(arr[9])
        html = obj['d']
        pattern = 'data:image/(\w+?);base64,([^\s]*?);'
        matches = re.findall(pattern, html, re.DOTALL)
        if matches:
            count = count + 1
            maxlen = 0
            # for i in range(len(matches)):
            imgstr = matches[0][1]
            # print imgstr
            imgstr = imgstr.replace('\\x27', '')
            imgstr = imgstr.replace('\\\\x3d', '=')
            imgmd5 = hashlib.md5(imgstr).hexdigest()
            # if imgmd5 in ignores: continue
            # maxlen = len(imgstr)
            # imgdata = base64.b64decode(imgstr)
            # newname = filename.split('.html')[0] + '.png'
            # with open('emblemgoogle/' + newname, 'wb') as f:
            #     f.write(imgdata)
            with open('google_test_2.html', 'w') as f:
                f.write(imgstr)
            # break
        else:
            print filename
            # break
    print count, len(files)

    # with open('google_test_2.html', 'w') as f:
        # f.writelines(prefix + matches[0].decode('utf-8'))
    return


def testGoogle(uniname, keyword, savedir='html_google'):
    import requests
    # url = "https://en.m.wikipedia.org/w/index.php?search=Universit%C3%A4t+Innsbruck"
    # url = "https://www.google.com.au/#newwindow=1&q=" + keyword
    keyword = keyword.replace(' ', '+')
    print keyword
    url = 'https://www.google.com.au/search?newwindow=1&q=' + keyword + '&bav=on.2,or.r_cp.&cad=b&fp=1&biw=1440&bih=458&dpr=1&tch=1&ech=1&psi=IwIcV_37HsPdmAW17qbQBQ.1461453350134.3'
    headers = {
        'referer':'https://www.google.com.au/',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    }
    res = requests.get(url, headers=headers)

    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = uniname + '.html'
    with open(savedir + '/' + filename, 'wb') as fd:
        for chunk in res.iter_content(100):
            fd.write(chunk)
    return


def scrapeGoogle(uniname, keyword, savedir='html_google_2'):
    from tornado_fetcher import Fetcher
    keyword = keyword.replace(' ', '+')
    print keyword
    url = 'https://www.google.com.au/#newwindow=1&q=' + keyword
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    fetcher = Fetcher(
        user_agent=user_agent,  # user agent
        phantomjs_proxy='http://localhost:12306',  # phantomjs url
        pool_size=10,  # max httpclient num
        async=False
    )
    res = fetcher.phantomjs_fetch(url)
    content = res['content'].encode('utf-8')
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    filename = uniname + '.html'
    with open(savedir + '/' + filename, 'wb') as fd:
        fd.write(content)
    return


def googleCrawler():
    from akaparser import loadData
    unilist = loadData('list_0423.csv')
    # uniname = 'Universidad Torcuato di Tella'
    # uniname = 'Universidad Nacional de Cordoba'
    count = 0
    for uni in unilist[1:]:
        img = uni[0] + '.png'
        if os.path.exists('emblem_0413/' + img):
            continue
        if os.path.exists('html_google_2/' + uni[0] + '.html'):
            continue
        uniname = uni[1]
        # print uni
        count = count + 1
        print count
        scrapeGoogle(uni[0], uniname)
        # break
    # print count
    return


def main():
    files = os.listdir('html_google_2/')
    if not os.path.exists('emblem_google/'):
        os.mkdir('emblem_google/')
    count = 0
    for filename in files:
        with open('html_google_2/' + filename, 'r') as f:
            html = f.read()
            doc = BeautifulSoup(html, 'lxml')
            tag_img = doc.select('#rhs_block a.bia img')
            if not tag_img:
                continue
            print filename
            img = tag_img[0]
            count = count + 1
            src = img['src'].split('base64,')[1]
            imgdata = base64.b64decode(src)
            newname = filename.split('.html')[0] + '.png'
            with open('emblem_google/' + newname, 'wb') as f:
                f.write(imgdata)

        # break
    print count
    return

if __name__ == '__main__':
    # scrapeGoogle()
    # main()
    # googleCrawler()