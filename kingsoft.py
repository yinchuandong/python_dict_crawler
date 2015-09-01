#encoding:utf-8

import os
import sys
import threading
import time

import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import base64
import json

g_cookie = cookielib.LWPCookieJar()
g_cookieFile = './cookies.dat'

g_mutex = threading.Condition()
g_queueUrl = [] #等待爬取
g_exsitUrl = [] #已经爬取
g_failedUrl = [] #爬取失败

class KingSoft(object):
    cookieFile = './cookies.dat'

    threadPool = []
    threadNum = 5

    def __init__(self):
        global g_cookie
        global g_queueUrl
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(g_cookie))
        urllib2.install_opener(opener)

        # g_queueUrl.append('hello')
        # g_queueUrl.append('world')
        # g_queueUrl.append('you')
        self.loadSeeds()
        return

    def loadSeeds(self):
        global g_queueUrl
        fhandle = open('oxford-words.txt', 'r')
        for line in fhandle.readlines():
            line = line.strip()
            g_queueUrl.append(line)
        # print g_queueUrl[10000]
        return

    def parse(self, html):
        doc = BeautifulSoup(html)
        # print doc
        # groupPos = doc.find('div', attrs={"class":"searchword_word_morphology"})
        # groupPos = doc.select('div.group_prons .group_pos ul')
        # print groupPos
        groupInf = doc.select('div.group_prons .group_inf ul')[0]

        # 判断该词是否有过去式过去分词等选项
        text = groupInf.select('li')[0].text.encode('utf-8')
        if "大家都在背" not in text:
            print groupInf
        print text
        return

    def downloadAll(self):
        global g_queueUrl
        i = 0
        while i < len(g_queueUrl):
            j = 0;
            #每次最多能创建 threadNum个线程
            while j < self.threadNum and i + j < len(g_queueUrl):
                self.download(g_queueUrl[i + j])
                j += 1
            i += j

            #挂起等待线程池中所有线程执行完毕
            for thread in self.threadPool:
                thread.join(30)
            threadPool = []
        return

    def download(self, word):
        thread = CrawlerThread(word)
        self.threadPool.append(thread)
        thread.start()
        return

class CrawlerThread(threading.Thread):
    word = None
    def __init__(self, word):
        threading.Thread.__init__(self)
        self.word = word
        return

    def run(self):
        global g_mutex
        global g_queueUrl
        global g_exsitUrl

        try:
            print 'crawlerthread is getting:', self.word
            # time.sleep(2)
            self.lookup(self.word)
        except Exception, e:
            g_mutex.acquire()
            g_exsitUrl.append(self.word)
            g_failedUrl.append(self.word)
            g_mutex.release()
            print 'fail to download or save: ', self.word
            print e

        g_mutex.acquire()
        g_exsitUrl.append(self.word)
        g_mutex.release()
        return

    def lookup(self, word):
        url = "http://www.iciba.com/" + word
        reqHeaders = {
            'Host': 'www.iciba.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,es;q=0.4,zh-TW;q=0.2,de;q=0.2'
        }

        req = urllib2.Request(url, headers=reqHeaders)
        res = urllib2.urlopen(req)
        html = res.read()
        html = html.decode('utf-8','replace').encode(sys.getfilesystemencoding())
        # info = res.info()
        if not os.path.exists('html'):
            os.makedirs('html')
        filepath = 'html/' + word + '.html';
        if os.path.exists(filepath):
            filepath = 'html/' + word + '_UPPER.html'
        fhandle = open(filepath, 'w')
        fhandle.write(html)
        fhandle.close()

        global g_cookie
        global g_cookieFile
        g_cookie.save(g_cookieFile)
        return

def run():
    model = KingSoft()
    model.lookup("Flavorful")
    return

def runAll():
    model = KingSoft()
    model.downloadAll()
    return

if __name__ == '__main__':
    # run()
    runAll()








