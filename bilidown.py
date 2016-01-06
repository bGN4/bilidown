# -*- coding: utf-8 -*- 

import os
import re
import time
import zlib
import gzip
import urllib2
import logging
import datetime
import StringIO

# deflate support
# zlib only provides the zlib compress format, not the deflate format;
# so on top of all there's this workaround:
def deflate(data):
    mode = 0
    while True:
        try:
            if mode==0:
                return zlib.decompress(data, -zlib.MAX_WBITS)
            elif mode==1:
                return zlib.decompress(data)
            else:
                return None
        except zlib.error as e:
            print(e)
            mode = mode + 1

def response_decode(response):
    buff = None
    encoding = response.headers.get('Content-Encoding')
    #print encoding
    if encoding == 'gzip':
        buff = gzip.GzipFile(fileobj=StringIO.StringIO( response.read() ),mode="r")
    elif encoding == 'deflate':
        buff = StringIO.StringIO( deflate( response.read() ) )
    else:
        buff = response
    return buff.read()

def getURL(url):
    headers  = {'Accept':'text/html,application/xhtml+xml,application/xml;', 'Accept-Encoding':'gzip,sdch',}
    request  = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request)
    result   = response_decode(response)
    return result

def readComment(fp):
    clist = []
    fp.seek(0, os.SEEK_SET)
    for line in fp.read().split('\n'):
        text = line.strip()
        if text:
            clist.append( text )
    print( 'READ : {} lines'.format(len(clist)) )
    return clist

def writeComment(fp, clist):
    fp.seek(0, os.SEEK_SET)
    fp.truncate(0)
    fp.write( '\n'.join(clist) )
    fp.flush()
    print( 'WRITE: {} lines'.format(len(clist)) )

def addComment(clist, data):
    pre_count = len(clist)
    while len(clist)>0 and clist[-1]=='</i>':
        clist = clist[:-1]
    for line in data.replace('</source><d p=', '</source>\n<d p=').split('\n'):
        text = line.strip()
        if text not in clist:
            clist.append( text )
    if len(clist)>0 and clist[-1]!='</i>':
        clist.append('</i>')
    now_count = len(clist)
    print( 'ADD  : {} lines'.format(now_count-pre_count) )
    return clist

def aid2avurl(aids):
    mobj = re.match('av(\d+)(?:#(\d+))?$', aids)
    result = 'http://www.bilibili.com/video/av{}/'.format(mobj.group(1))
    if ('%s'%mobj.group(2)).isdigit():
        result = result + 'index_{}.html'.format(mobj.group(2))
    return result

def avurl2aid(avurl):
    mobj = re.match('http://www.bilibili.com/video/av(\d+)/(?:index_(\d+).html)?$', avurl)
    result = 'av{}'.format(mobj.group(1))
    if ('%s'%mobj.group(2)).isdigit():
        result = result + '#{}'.format(mobj.group(2))
    return result

def getXmlURL(avurl):
    html = getURL( avurl )
    sobj = re.search('"http://static.hdslb.com/play.swf",\s*"cid=(\d+)&aid=(\d+)"', html)
    return 'http://comment.bilibili.com/{}.xml'.format(sobj.group(1))

def rollingComment(url):
    urlc = getXmlURL( url )
    File = avurl2aid( url ) + '.xml'
    print( '{} > {}'.format(urlc, File) )
    with open(File, 'a+') as fp:
        for i in range(100):
            clist = readComment(fp)
            data  = getURL(urlc)
            clist = addComment(clist, data)
            writeComment(fp, clist)
            for i in range(10*60):
                time.sleep(1)

if __name__ == '__main__':
    rollingComment( 'http://www.bilibili.com/video/av3511392/index_1.html' )
