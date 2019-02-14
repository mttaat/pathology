#!/usr/bin/python
#
# Copyright (c) 2019 mttaat <mttaat@protonmail.com>. All Rights Reserved.
# This file licensed under the GPLv3
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# pathology v0.1
# path-based web fuzzer
#
# usage: $ python pathology -d <domains,domains> -p <pathlist> -s '<success regex>' -f '<fail regex>' -x <file extension,file extension> -o <outputfile>
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

def usage():
    print("usage: $ python pathology -d <domains,domains> -p <pathlist> -s '<success regex>' -f '<fail regex>' -x <file extension,file extension> -o <outputfile>");
    sys.exit()

def passfail(response, success, failure):
    print(response)

def domlist():
    print("")

def pathlist():
    print("")

def request():
    print("")


if len(sys.argv) < 4:
    usage()
