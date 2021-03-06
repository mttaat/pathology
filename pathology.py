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
from requests import exceptions
import argparse
import string

def passfail(response, success, failure):
    print(response)

def targetlist():
    targetlist = str(arguments['t'])
    targets = []

# rework this logic:
# if targetlist is a file, parse it,
# otherwise do the split
# (currently requires janky appending of a comma for a single domain scan)

    if string.find(targetlist, '/') != -1:
        f = open(targetlist, 'r')
        for line in f:
            if string.find(line, '#') != 0:
                targets.append(string.strip(line))
    elif string.find(targetlist, ',') != -1:
        targets = targetlist.split(',')
    else:
        targets = [targetlist]

    return targets

def pathlist():
    pathlist = str(arguments['l'])
    paths = []
    # TODO: percent encode unicode chars rather than strip them out
    strip_unicode = re.compile("([^-_a-zA-Z0-9!@#%&=,/'\";:~`\$\^\*\(\)\+\[\]\.\{\}\|\?\<\>\\]+|[^\s]+)")
    if string.find(pathlist, ',') == -1:
        f = open(pathlist, 'r')
        for line in f:
            if string.find(line, '#') != 0:
                line = string.strip(line)
                line = strip_unicode.sub('',line)
                if line != '':
                    paths.append(string.strip(line))
    else:
        paths = pathlist.split(',')

#    print(paths)
    return paths

def methodlist():
    methodlist = str(arguments['m'])
    methods = methodlist.split(',')
    return methods

def protocollist():
    protocollist = str(arguments['p'])
    protocols = protocollist.split(',')
    return protocols

def request(proto, method, target, path):
    r = None
    uri = string.lower(proto + '://' + target + '/' + path)
    print('==== Request ' + method + ' ' + uri + " ====")
    requestmethod = getattr(requests, string.lower(method))
    try:
        r = requestmethod(uri, verify=False)
    except exceptions.RequestException as e:
        print("ERROR: " + str(e))
    return r

# TODO: support all arguments
# TODO: multithreading and map

def loopbody():
    paths = pathlist()
    targets = targetlist()
    methods = methodlist()
    protocols = protocollist()

    # TODO: refactor for multithreading
    for t in targets:
        for h in protocols:
            for p in paths:
                for m in methods:
                    try:
                        response = request(h, m, t, p)
                        print(response)
                        if arguments['f']:
                            if response and (string.count(str(response.text), str(arguments['f'])) == 0):
                                print('+++PASSED+++')
                                print(response.text)
                        else:
                            print(response.text)
                    except KeyboardInterrupt:
                        sys.exit()

parser = argparse.ArgumentParser(
                version='0.1', 
                description='Modern web path fuzzer',
                epilog='')

parser.add_argument('-t', action='store', help='domain/IP list, comma-separated (cli) or newline separated (file)')
parser.add_argument('-l', action='store', help='list to generate paths with, comma-separated (cli) or newline-separated (file)', default=None)
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
parser.add_argument('-f', action='store', help="failure regex", default=None)
parser.add_argument('-e', action='store', help='file extensions list', default=None)

              
try:
    arguments = vars(parser.parse_args())

except IOError, msg:
    parser.error(str(msg))

if not arguments['t'] or not arguments['l']:
    parser.print_help() 
    sys.exit()

loopbody()
