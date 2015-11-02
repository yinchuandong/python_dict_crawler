#encoding:utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
# import MySQLdb
import pymysql

from bs4 import BeautifulSoup


apkList = []

def getConn():
    conn = None
    try:
        conn=pymysql.connect(host='localhost',user='root',passwd='123',db='mytablet',port=3306,charset='utf8')
    except pymysql.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return conn

def init():
    fhandle = open('../out/appsearch.json', 'w')
    conn = getConn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    count = cursor.execute("select * from mytablet as t")
    results = cursor.fetchall()
    for item in results:
        apkList.append(item)

    fhandle.write(json.dumps(apkList)) 
    fhandle.close()
    print count
    print results

    cursor.close()
    conn.close()
    return

if __name__ == '__main__':
    print sys.getdefaultencoding()
    init()



