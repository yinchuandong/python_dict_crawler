#encoding:utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import MySQLdb

from bs4 import BeautifulSoup

categoryDict = {}
subjectDict = {}
typeDict = {}


def getConn():
    conn = None
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123',db='stra',port=3306,charset='utf8')
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return conn

def init(categoryName):
    conn = getConn()
    cursor = conn.cursor()
    count = cursor.execute("select * from st_category")
    results = cursor.fetchall()
    for item in results:
        id = item[0]
        name = item[1]
        categoryDict[name] = id
        # print id, name

    cursor = conn.cursor()
    count = cursor.execute("select * from st_subject")
    results = cursor.fetchall()
    for item in results:
        id = item[0]
        name = item[1]
        subjectDict[name] = id
        print id, name

    categoryId = categoryDict[categoryName.decode('utf-8')]
    cursor = conn.cursor()
    count = cursor.execute("select * from st_type as t where t.categoryId=" + bytes(categoryId))
    results = cursor.fetchall()
    for item in results:
        id = item[0]
        name = item[1]
        typeDict[name] = id
        # print id, name

    print '------------科目加载完毕--------------'
    return

def parseJaocaiOrDiandu(filepath, categoryName, ext):
    """
    @param {string} filepath: 文件路径
    @param {string} categoryName: 如，同步教材
    @param {string} ext: 目标文件的后缀，如JCD, xlc等
    """
    file = open(filepath)
    lines = file.readlines()

    conn = getConn()
    cursor = conn.cursor()
    i = 0
    for line in lines:
        line = line.decode('gbk').encode('utf-8')
        # print line
        # break
        lineArr = line.split(",")
        fullName = lineArr[2].replace('"','');
        html = BeautifulSoup(lineArr[3])
        divTags = html.select('div div div')

        print len(divTags)
        if len(divTags) != 11:
            print '-----------------------------------'
            print '-----------------------------------'
            print html
            continue

        # 解析出版社等信息
        name = divTags[0].string
        publisher = divTags[4].string.split(':')[1]
        publisherInfoArr = divTags[6].string.split(':')
        publisherInfo = ''
        if len(publisherInfoArr) == 2:
            publisherInfo = publisherInfoArr[1]
        textbookNo = divTags[8].string.split(':')[1]
        

        subjectName = lineArr[4].replace('"','')
        typeName = lineArr[5].replace('"','')
        uploadTime = lineArr[9]
        count = lineArr[10].split('.')[0]

         # 解析a标签中的超链接,需要手动把文件中得""替换成"，否则无法解析a标签
        linkUrl = divTags[10].a['href']
        spos = linkUrl.rfind('/') + 1
        epos = linkUrl.rfind('.')
        filename = linkUrl[spos:epos] + '.' + ext
        url = categoryName + '/' + subjectName + '/' + typeName + '/' + filename

        categoryId = categoryDict[categoryName.decode('utf-8')]
        subjectId = subjectDict[subjectName.decode('utf-8')]
        typeId = typeDict[typeName.decode('utf-8')]

        print categoryId, subjectId, typeId, fullName, name, \
            publisher, publisherInfo, textbookNo, filename, url, \
            uploadTime, count
        
        params = [categoryId, subjectId, typeId, fullName, name, \
            publisher, publisherInfo, textbookNo, filename, url, \
            uploadTime, count]
        sql = 'insert into st_tutorial (categoryId, subjectId, typeId, fullName, name, \
            publisher, publisherInfo, textbookNo, filename, url, \
            uploadTime, count) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, params)
        print sql
        # break

    conn.commit()
    cursor.close()
    conn.close()
    file.close()
    return

if __name__ == '__main__':
    print sys.getdefaultencoding()

    # init('同步教材')
    # parseJaocaiOrDiandu('../9000/教材/News.txt', '同步教材', 'xlc')
    # init('课文点读')
    # parseJaocaiOrDiandu('../9000/点读/News.txt', '课文点读', 'JCD')



