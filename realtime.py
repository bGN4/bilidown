# -*- coding: utf-8 -*- 
from __future__ import print_function
import os
import re
import sys
import time
import socket
import struct
import binascii
import urlparse

fillen = lambda f1,f2,body: struct.pack('!BBH', f1, f2, 4+len(body)) + body

CID = 11645168
HOST = 'chat.bilibili.com'
PORT = 88
chat0 = fillen(1, 1, struct.pack('!I4s', 11645168, ''))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect((HOST, PORT))
s.sendall(chat0)
while True:
    try:
        data = s.recv(1024)
        (f1, f2, lenth) = struct.unpack('!BBH', data[:4])
        if (f1,f2)==(0,2):
            print(data[4:])
        elif (f1,f2)==(0,1):
            print(lenth, struct.unpack('!H', data[4:]), struct.unpack('H', data[4:]))
        else:
            print(repr(data))
    except socket.timeout as e:
        chat1 = fillen(1, 4, struct.pack('!4s', ''))
        s.sendall(chat1)
s.close()


