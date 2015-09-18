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


def getConn():
    conn = None
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='123',db='stra',port=3306,charset='utf8')
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return conn

def init():
    conn = getConn()
    cursor = conn.cursor()
    count = cursor.execute("select * from st_category")
    results = cursor.fetchall()
    for item in results:
        id = item[0]
        name = item[1]
        categoryDict[name] = id
        print id, name

    cursor = conn.cursor()
    count = cursor.execute("select * from st_subject")
    results = cursor.fetchall()
    for item in results:
        id = item[0]
        name = item[1]
        subjectDict[name] = id
        print id, name

    print '------------科目加载完毕--------------'
    return

def parseJaocaiOrDiandu(filepath, categoryName):
    """
    @param {string} filepath: 文件路径
    @param {string} categoryName: 如，同步教材
    """
    file = open(filepath)
    lines = file.readlines()

    conn = getConn()
    cursor = conn.cursor()

    for line in lines:
        line = line.decode('gbk').encode('utf-8')
        lineArr = line.split(",")
        id = lineArr[0]
        name =  lineArr[1].replace('"','')
        subject = lineArr[2].replace('"', '')

        params = [name, categoryDict[categoryName.decode('utf8')], subjectDict[subject.decode('utf-8')]]
        cursor.execute('insert into st_type (name, categoryId, subjectId) values (%s, %s, %s)', params)
        print id, name, subject

    conn.commit()
    cursor.close()
    conn.close()
    file.close()
    return

if __name__ == '__main__':
    print sys.getdefaultencoding()

    init()
    # parseJaocaiOrDiandu('../9000/教材/SmallClass.txt', '同步教材')
    # parseJaocaiOrDiandu('../9000/点读/SmallClass.txt', '课文点读')



