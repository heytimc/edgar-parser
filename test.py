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

try:
  # check arguments
  if len(sys.argv) != 2:
    print('Startup arguments incorrect. Please provide: filename')
    exit(1)

  # connect to database
  filename = sys.argv[1]

  print('starting test run with file {0}'.format(filename))
  response = urllib.request.urlopen('file:' + filename)
  html = response.read()
  parser = Edgarparser.Edgarparser()
  print(parser.def14a(html))

except Exception as e:
  print("Aborted: {0}".format(e.args[0]))
  sys.exit(1)