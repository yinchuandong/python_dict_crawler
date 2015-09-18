#encoding:utf-8

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
# import MySQLdb
import pymysql

from bs4 import BeautifulSoup


noneFileList = []

def getConn():
    conn = None
    try:
        conn=pymysql.connect(host='localhost',user='root',passwd='123',db='stra',port=3306,charset='utf8')
    except pymysql.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return conn

def init():
    dataPath = '/Users/yinchuandong/Downloads/9000/'
    file = open('noneFileList.txt', 'w')
    conn = getConn()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    count = cursor.execute("select * from st_tutorial as t where t.categoryId=1")
    results = cursor.fetchall()
    for item in results:
        fullName = item['fullName']
        url = item['url']
        path = dataPath + url
        if not os.path.exists(path):
            noneFileList.append((fullName, url))
            print fullName,url
            file.writelines(fullName + ',' + url + '\n\r')
        
        # break
    file.flush()
    file.close()
    cursor.close()
    conn.close()
    return


if __name__ == '__main__':
    print sys.getdefaultencoding()
    init()



