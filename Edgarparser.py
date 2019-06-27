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
#                 find for meeting herald text
#
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
  """return structured data from html-rich EDGAR message"""
  logger = logging.getLogger('Edgarparser')

  ########################################################################################
  def __init__(self):
#   logging.basicConfig(format=LOGFORMAT)
    logging.basicConfig(level=LOG_CURRENT_MINIMUM)



  ########################################################################################
  def stripHtmlTags(self, htmlTxt):
    """strip html tags from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""
    try:
      if htmlTxt is None:
        return None
      else:
        return ''.join(BeautifulSoup(htmlTxt, 'lxml').findAll(text=True))
    except Exception as e:
      raise e.args[0]



  ########################################################################################
  # parse a def14a html message
  def def14a(self, html):
    try:
      # init in case we can't find them or precursor
      meetingherald = ""
      meetingyear = ""

      self.logger.log(LOG_INFO, "Parsing started")

      soup = BeautifulSoup(html, 'lxml') # very lenient, slow parsing
      # find the start of the meeting notice
      meetingherald = soup.find(string=re.compile("(?i)notice.*of.*meeting.*of.*stockholders"))
      if not meetingherald:
        raise def14aError("No meeting herald line found")

      # find the meeting year (exactly four digits starting with "2") within the herald text
      self.logger.log(LOG_DEBUG, "Meeting herald found: {0}".format(meetingherald.strip()))
      meetingyear = re.findall("2\d{3}", meetingherald)
      if not meetingyear:
        raise def14aError("No meeting year found")

      # now we iterate over the text from the herald onwards
      item = meetingherald
      lastitem = "" # .next_item seem to repeat....?!
      loop = 0
      while item != None:

        item = item.next_element

        # cleanup
        lastitem = str(item).strip().replace('\n', ' ')

        # ignore empty lines
        if len(lastitem) < 1 or lastitem[0] == '<':
          ++loop
          continue

        self.logger.log(LOG_DEBUG, "debug found {0} {1}".format(loop, lastitem[:70]))
        ++loop

      result = "".join(meetingherald), meetingyear

    except def14aError as e:
      raise Exception(e.args[0])
    except Exception as e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      self.logger.log(LOG_CRITICAL, "Abort during processing")
      self.logger.log(LOG_CRITICAL, sys.exc_info())
      imported_tb_info = traceback.extract_tb(exc_traceback)[-1]
      line_number = imported_tb_info[1]
      self.logger.log(LOG_CRITICAL, "at line number " + str(line_number))
      sys.exit(1)

    finally:
      self.logger.log(LOG_INFO, "Parsing finished")

    return result
