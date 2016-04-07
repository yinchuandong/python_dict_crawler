import os
import sys
import time
import struct

class Person(object):
    f_name = ''
    l_name = ''
    age = 0

    def __init__(self):
        return

def readBin(filename):
    fIn = open(filename, 'rb')
    fIn.seek(0, 0)
    fileSize = os.path.getsize(filename)
    print "file size is: ", fileSize
    # tmp = fIn.read(sys.getsizeof(Person))
    tmp =  fIn.read(4)
    count = struct.unpack('i', tmp)
    print count

    
    tmp = fIn.read(256 + 256 + 4)
    while len(tmp) > 0:
        result = struct.unpack('256c256ci', tmp)
        f_name = ''.join(result[0:255]).replace("\x00", '')
        l_name = ''.join(result[256:511]).replace("\x00", '')
        age = result[512]
        print f_name, l_name, age
        print len(tmp)
        tmp = fIn.read(256 + 256 + 4)

    fIn.close()
    return

def readText(filename):
    fIn = open(filename, 'r')
    content = fIn.read()
    print len(content)
    fIn.close()
    return

if __name__ == '__main__':
    startTime = time.clock()
    # readBin("/Users/yinchuandong/cproject/stra/stra/data.bin")
    readText('out/wordList.json')
    endTime = time.clock()

    print "delay time is : %f s" % (startTime - endTime)





