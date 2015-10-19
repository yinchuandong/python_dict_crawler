#encoding:utf-8

import os
import sys
import time
import json

wordArr = None
wordMap = {}

def run():
    inFile = open('out/wordList.json', 'r')
    jsonStr = inFile.read()
    inFile.close()

    wordArr = json.loads(jsonStr)
    # print wordArr[0]

    outFile = open('out/newList.json', 'w')
    for wordObj in wordArr:
        word = wordObj['word']
        wordMap[word] = wordObj
        outFile.write(json.dumps(wordObj) + "\n")
        # break

    tmpstr = wordMap['like']
    newList = []
    newList.append(tmpstr)
    
    # outFile.write(json.dumps(newList))
    outFile.close()
    return

if __name__ == '__main__':
    run()







