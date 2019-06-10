#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# test.py
#
# created by:   Tim Clarke
# date:         8jun2019
# change log:
# purpose:      call edgar message parser with test data
#
#               pseudo-code:
#
#
# returns:      prints test results
# errors:
# assumes:
# side effects:
#
# Maintenance:
#
# version:
# by:
# date:
# change log:
# purpose:
#

import sys
if sys.version_info[0] < 3:
  raise Exception("Please run using Python 3")
import urllib.request
import Edgarparser

print('starting')
response = urllib.request.urlopen('file:test.htm')
html = response.read()
parser = Edgarparser.Edgarparser()
print(parser.def14a(html))