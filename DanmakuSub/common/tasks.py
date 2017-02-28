#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import json
import codecs
import socket
import random
import shutil
import logging
import sqlite3
import datetime
import argparse
import traceback
import subprocess
try:
    from bilidown import *
except ImportError:
    sys.path.append('../../')
    sys.path.append('D:/home/site/repository')
    from bilidown import *

def update_bili_comment(dbpath, comment, oldnum, dm_max, nownum):
    (pk, cid) = (comment["id"], comment["cid"])
    ltime = datetime.datetime.strptime(comment["ltime"], '%Y-%m-%d %H:%M:%S')
    dm_max = getnum
    now = datetime.datetime.now()
    every = (now-ltime).total_seconds()/(nownum-oldnum) if nownum>oldnum else 0
    estimate = dm_max*every*0.5
    spent = 600 if estimate<600 else 3600 if estimate>3600 else estimate
    nxt = (now+datetime.timedelta(seconds=estimate)).strftime('%Y-%m-%d %H:%M:%S')
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cmd = 'UPDATE bili_comment SET cid="%s",count="%s",ltime="%s",ntime="%s" WHERE id=%s'%(cid,nownum,now,nxt,pk)
    logging.info( '[{},{},{},()] '.format(ltime,every,estimate,spent)+cmd )
    cursor.execute( cmd )
    cursor.commit()

def get_files_of_dir(path):
    for rr,dd,ff in os.walk(path):
        return [os.path.join(rr,f) for f in ff]

def load_jsonfile(path):
    with open(path) as fp:
        return json.load(fp)

def get_cid_by_avid(aid, pid=1):
    avurl = 'http://www.bilibili.com/video/av%s/index_%s.html'%(aid,pid)
    xmlurl = getXmlURL(avurl)
    return xmlurl[xmlurl.rfind('/')+1:-4]

def refresh_cid_xml(cid, path):
    xmlurl = 'http://comment.bilibili.com/{}.xml'.format(cid)
    logging.info(xmlurl)
    with codecs.open(path, 'a+', encoding='utf8') as fp:
        clist = readComment(fp)
        oldnum= len(clist)
        data  = getURL(xmlurl)
        getnum= len(data)
        clist = addComment(clist, data)
        nownum= len(clist)
        writeComment(fp, clist)
        return (oldnum, getnum, nownum)

def process_file(jsonpath, dbpath, xmlpath):
    logging.info(jsonpath)
    comment = load_jsonfile(jsonpath)
    if len(comment["cid"])<3:
        comment["cid"] = get_cid_by_avid(comment["aid"], comment["pid"])
    (oldnum, getnum, nownum) = refresh_cid_xml(comment["cid"], xmlpath)
    update_bili_comment(dbpath, comment, oldnum, getnum, nownum)
    os.remove(f)
    return random.randint(2,6)

def proc(basedir):
    queuedir = os.path.join(basedir, 'queue')
    down_dir = os.path.join(basedir, 'download')
    if not os.path.isdir(queuedir): os.mkdir(queuedir)
    if not os.path.isdir(down_dir): os.mkdir(down_dir)
    while True:
        for f in get_files_of_dir(queuedir):
            try:
                delay = process_file(f, os.path.join(basedir, 'db.sqlite3'), os.path.join(down_dir, 'av%s#%s.xml'%(aid,pid)))
                time.sleep( delay )
            except Exception as e:
                logging.error( traceback.format_exc() )
        time.sleep(1)


if __name__ == '__main__':
    timenow = time.strftime('%Y%m%d%H%M%S')
    execdir = os.path.dirname(os.path.abspath(__file__))
    currdir = os.path.abspath(os.curdir)
    basedir = 'D:/home/site/wwwroot'
    logfile = os.path.join(basedir, 'debug-task.log')
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s #%(levelname).1s %(process)5d [%(filename)12s:%(lineno)04d] -> %(message)s',
                        filename=logfile, filemode='a')
    logging.debug(currdir)
    try:
        proc(basedir)
    except Exception as e:
        logging.error( traceback.format_exc() )

