#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# edgarparser.py
#
# created by:   Tim Clarke
# date:         8jun2019
# change log:
# purpose:      return structured data from edgar message blob (html-rich edgar scraping)
#
#               pseudo-code:
#
#
# returns:      specifically-structured array for the given message
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
import datetime, logging
from time import gmtime, strftime
from bs4 import BeautifulSoup


########################################################################################
# constants
# logging constants
LOGFORMAT = '%(asctime)-15s %(message)s'
LOG_DEBUG = 10
LOG_INFO = 20
LOG_WARNING = 30
LOG_ERROR = 40
LOG_CRITICAL = 50
# current logging minimum level for the run
LOG_CURRENT_MINIMUM = LOG_DEBUG


class Edgarparser(object):
  'return structured data from html-rich EDGAR message'
  logger = logging.getLogger('edgarparser')

  ########################################################################################
  def __init__(self):
    logging.basicConfig(format=LOGFORMAT)
    Edgarparser.logger.setLevel(LOG_CURRENT_MINIMUM)


  ########################################################################################
  # logger
  def _log(self, level, message):
    Edgarparser.logger.log(level, message)


  ########################################################################################
  # parse a def14a html message
  def def14a(self, html):
    try:
      self._log(LOG_DEBUG, "Parsing def14a started")
      soup = BeautifulSoup(html, 'html5lib')
      text = soup.get_text()
      tokens = [t for t in text.split()]
      self._log(LOG_DEBUG, "Parsing def14a finished")
    except SyntaxError as e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      log(LOG_CRITICAL, "Abort during processing {0} at line {1}".format(str(exc_value), str(exc_traceback.tb_lineno)))
    except Exception as e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      log(LOG_CRITICAL, "Abort during processing")
      log(LOG_CRITICAL, sys.exc_info())
      imported_tb_info = traceback.extract_tb(exc_traceback)[-1]
      line_number = imported_tb_info[1]
      log(LOG_CRITICAL, "at line number " + str(line_number))
      sys.exit(1)
    return text
