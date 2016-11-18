# -*- coding: utf-8 -*- 
from __future__ import print_function
import os
import re
import sys
import time
import zlib
import gzip
import codecs
import urllib2
import logging
import datetime
import StringIO
import argparse
import itertools
from xml.etree import ElementTree

def XMLNode(tag, *kids, **attrs):
    n = ElementTree.Element(tag, attrs)
    for k in kids:
        if isinstance(k, basestring):
            assert n.text is None
            n.text = k
        else:
            n.append(k)
    return n

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

def getURL0(url):
    headers  = {'Accept':'text/html,application/xhtml+xml,application/xml;', 'Accept-Encoding':'gzip,sdch',}
    request  = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request)
    result   = response_decode(response)
    return result

def getURL(url):
    import requests
    headers  = {'Accept':'text/html,application/xhtml+xml,application/xml;', 'Accept-Encoding':'gzip,sdch',}
    response = requests.get(url, headers=headers)
    return response.text

def safe_cast(val, to_type, default=None):
    try: return to_type(val)
    except: return default

def getTime(comment, prog=re.compile('<d p="([\d.]+),')):
    try: return float( prog.match(comment).group(1) )
    except: return 0.0

def readComment(fp):
    clist = []
    fp.seek(0, os.SEEK_SET)
    for line in fp.read().split('\n'):
        text = line.strip()
        if text:
            clist.append( text )
    print( 'READ : {} lines'.format(len(clist)) )
    return clist

def parseComment(text):
    parser = ElementTree.XMLTreeBuilder()
    parser.feed( text.encode('utf8') )
    root = parser.close()
    return root

def mergeComment(root1, root2):
    root = root1
    return root

def writeComment(fp, clist):
    fp.seek(0, os.SEEK_SET)
    fp.truncate(0)
    fp.write( u'\n'.join(clist) )
    fp.flush()
    print( 'WRITE: {} lines'.format(len(clist)) )

def addComment(clist, data):
    pre_count = len(clist)
    clist2 = data.replace(u'</source><d p=', u'</source>\n<d p=').split(u'\n')
    clist2_clean = itertools.imap(lambda x: x.strip(), clist2)
    clist2_comment = set(itertools.ifilter(lambda x: x.startswith(u'<d p='), clist2_clean))
    clist1_comment = set(itertools.ifilter(lambda x: x.startswith(u'<d p='), clist))
    clist1_header  = clist[0] if pre_count>0 and clist[0].startswith(u'<?xml') else u'<?xml version="1.0" encoding="UTF-8"?><i>'
    clist2_header  = clist2[0].strip() if len(clist2)>0 and clist2[0].strip().startswith(u'<?xml') else u''
    clist = [(clist1_header, clist2_header)[len(clist2_header)>len(clist1_header)],] + sorted(clist1_comment|clist2_comment, key=getTime) + [u'</i>',]
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
    try:
        html = getURL( avurl )
        sobj = re.search('"http://static.hdslb.com/play.swf",\s*"cid=(\d+)&aid=(\d+)', html)
        if sobj is None:
            sobj = re.search('bili-cid=(\d+)', html)
        #print(sobj.groups())
        return 'http://comment.bilibili.com/{}.xml'.format(sobj.group(1))
    except:
        print('ERROR IN getXmlURL(avurl="{0}")'.format(avurl), file=sys.stderr)
        print(html)
        raise

def rollingComment(url, count=100):
    urlc = getXmlURL( url )
    File = avurl2aid( url ) + '.xml'
    print( '{} > {}'.format(urlc, File) )
    with codecs.open(File, 'a+', encoding='utf8') as fp:
    #with open(File, 'a+') as fp:
        for i in range(count):
            clist = readComment(fp)
            data  = getURL(urlc)
            clist = addComment(clist, data)
            writeComment(fp, clist)
            for i in range(30*60):
                time.sleep(1)

def genURL(url_in):
    url_out = url_in
    for pattern in [b'^(av\d+)(?:#(\d+))?$', b'(av\d+)/(?:index_(\d+).html)?$']:
        obj = re.search(pattern, url_in)
        if obj is not None:
            url_out = 'http://www.bilibili.com/video/{}/index_{}.html'.format(obj.group(1), safe_cast(obj.group(2),int,1))
            break
    print(url_out)
    return url_out

def getopt():
    parser = argparse.ArgumentParser(description='Download comments from bilibili.')
    parser.add_argument('url', help='URL of bilibili')
    parser.add_argument('-c', '--count', type=int, default=100, help='counter (default: 100)')
    return parser.parse_args()

if __name__ == '__main__':
    count = 100
    url   = 'http://www.bilibili.com/video/av4954199/index_1.html'
    if len(sys.argv)>1:
       opt = getopt()
       url = genURL(opt.url)
       count = opt.count
    rollingComment(url, count)

