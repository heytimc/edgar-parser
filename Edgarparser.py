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
import datetime, logging, re, traceback
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

class def14aError(RuntimeError):
  pass

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
  # strip html tags
  # from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
  def stripHtmlTags(self, htmlTxt):
    try:
      if htmlTxt is None:
        return None
      else:
        return ''.join(BeautifulSoup(htmlTxt, 'html5lib').findAll(text=True))
    except Exception as e:
      print(e.args[0])



  ########################################################################################
  # parse a def14a html message
  def def14a(self, html):
    try:
      # init in case we can't find them or precursor
      meetingherald = ""
      meetingyear = ""

      self._log(LOG_DEBUG, "Parsing started")

      soup = BeautifulSoup(html, 'html5lib') # very lenient, slow parsing
      # find the start of the meeting notice
      meetingherald = soup.find(text=true, string=re.compile("(?i)notice.of.*meeting.*of.*stockholders"))
      if not meetingherald:
        raise def14aError("No meeting herald line found")
      else:
        print(meetingherald)
        # find the meeting year within the herald text
        meetingyear = re.findall("[0-9]{4}", meetingherald)
        item = meetingherald
        # now we iterate from here
        for loop in range(20):
          item = item.next_element
          displayitem = self.stripHtmlTags(str(item))
          print("next {0} {1}".format(loop, displayitem))
      result = "".join(meetingherald), meetingyear

    except def14aError as e:
      raise Exception(e.args[0])
    except Exception as e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      self._log(LOG_CRITICAL, "Abort during processing")
      self._log(LOG_CRITICAL, sys.exc_info())
      imported_tb_info = traceback.extract_tb(exc_traceback)[-1]
      line_number = imported_tb_info[1]
      self._log(LOG_CRITICAL, "at line number " + str(line_number))
      sys.exit(1)

    finally:
      self._log(LOG_DEBUG, "Parsing finished")

    return result