#!/usr/bin/python
#
# Copyright (c) 2019 mttaat <mttaat@protonmail.com>. All Rights Reserved.
# This file licensed under the GPLv3
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# pathology v0.1
# 'modern' (2019) path-based web fuzzer
#
# # # # # # # # 
#
# @mttaat
# https://mttaat.net
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sys
import re
import requests
import argparse
import string

#def usage():
#    print("usage: $ python pathology -d <domains,domains> -p <pathlist> -s '<success regex>' -f '<fail regex>' -x <file extension,file extension> -o <outputfile>");
#    sys.exit()

def passfail(response, success, failure):
    print(response)

def targetlist():
    targetlist = str(arguments['t'])
    targets = targetlist.split(',')
    return targets

def pathlist():
    pathlist = str(arguments['l'])
    paths = pathlist.split(',')
    return paths

def methodlist():
    methodlist = str(arguments['m'])
    methods = methodlist.split(',')
    return methods

def request(method, target, path):
    r = None
    if method == 'GET':
        uri = string.lower(str(arguments['p'])) + '://' + target + '/' + path
        print('Requesting ' + method + ' ' + uri)
        r = requests.get(uri)
    return r

# TODO: support all arguments
# TODO: multithreading and map

def loopbody():
    paths = pathlist()
    targets = targetlist()
    methods = methodlist()

    # TODO: refactor for multithreading
    for t in targets:
        for p in paths:
            for m in methods:
                response = request(m, t, p)
                print response

parser = argparse.ArgumentParser(
                version='0.1', 
                description='Modern web path fuzzer',
                epilog='')

parser.add_argument('-t', action='store', help='domain/IP list, comma-separated')
parser.add_argument('-l', action='store', help='list to generate paths with, comma-separated', default=None)
parser.add_argument('-p', action='store', help='protocol: HTTPS (default) or HTTP', default='https')
#parser.add_argument('-l', action='store', help='list to generate paths with, comma-separated', default="pathlist.txt")
parser.add_argument('-m', action='store', help='list of HTTP methods (GET, HEAD, etc) to use', default="GET")
#parser.add_argument('-x', action='store', help='list of file extensions', default=None)
#parser.add_argument('-o', action='store', help='output file', default="pathology_output.txt")
#parser.add_argument('-n', action='store', help='number of threads', default="5")
#parser.add_argument('-p', action='store', help='proxy host:post')
#parser.add_argument('-a', action='store', help='HTTP auth username:password')
#parser.add_argument('-c', action='store', help='cookie', default=None)
#parser.add_argument('-u', action='store', help='user-agent', default="Mozilla/5.0")
#parser.add_argument('-V', action='store_true', help="verbose output")
parser.add_argument('-s', action='store', help="success regex", default=None)
parser.add_argument('-f', action='store', help="failure regex", default=None)

try:
    arguments = vars(parser.parse_args())

except IOError, msg:
    parser.error(str(msg))

if not arguments['t'] or not arguments['l']:
    parser.print_help() 
    sys.exit()

loopbody()
