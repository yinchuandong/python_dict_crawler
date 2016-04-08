# coding:utf-8

import os
import sys
import json

from bs4 import BeautifulSoup


class KingSoftParser(object):

    wordList = []

    def __init__(self):

        return

    def run(self):
        if not os.path.exists('out'):
            os.makedirs('out')

        fList = os.listdir('html')
        i = 0
        for filename in fList:
            file = open('html/' + filename, 'r')
            html = file.read()
            word = ''
            if '_' in filename:
                word = filename.split('_')[0]
            else:
                word = filename.split('.')[0]
            # print word
            self.parse(word, html)
            file.close()
            i += 1
            # if i > 10:
            #     break
            if i % 100 == 0:
                print "current process is : ", i

        print self.wordList
        fOut = open('out/wordList.json', 'w')
        fOut.write(json.dumps(self.wordList))
        fOut.close()
        return


    def parse(self, word, html):
        wordObj = {}
        wordObj['word'] = word

        doc = BeautifulSoup(html)
        #解析 词性和词义
        groupPos = doc.select('div.group_prons .group_pos')
        if len(groupPos) == 0:
            return;
        groupPos = groupPos[0]
        posTagList = groupPos.select('strong.fl')
        expTagList = groupPos.select('span.label_list')
        posList = []
        for posTag, expTags in zip(posTagList, expTagList):
            pos = posTag.text
            expList = []
            expTags = expTags.select('label')
            for expTag in expTags:
                expList.append(expTag.text)
            posObj = {
                pos: expList
            }
            # print posObj
            posList.append(posObj)
        wordObj['pos'] = posList

        #解析 不同的变换形式
        groupInf = doc.select('div.group_prons .group_inf ul')
        if len(groupInf) == 0:
            return

        groupInf = groupInf[0]
        # 判断该词是否有过去式过去分词等选项
        flagText = groupInf.select('li')[0].text.encode('utf-8')
        # 代表groupInf第0个为单词的集中变换形式
        if "大家都在背" not in flagText:
            liTags = groupInf.select('li')

            for liTag in liTags:
                aText = liTag.find('a').text
                if u"复数" in liTag.text:
                    wordObj['plural'] = aText
                if u"过去式" in liTag.text:
                    wordObj['pt'] = aText
                if u"过去分词" in liTag.text:
                    wordObj['p.p'] = aText
                if u"现在分词" in liTag.text:
                    wordObj['p.pr'] = aText
                if u"第三人称单数" in liTag.text:
                    wordObj['3ps'] = aText
        # print wordObj
        # print '----------------'
        self.wordList.append(wordObj)
        return








if __name__ == '__main__':
    parser = KingSoftParser()
    parser.run()












