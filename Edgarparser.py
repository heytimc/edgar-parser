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
import datetime, logging, re, traceback, collections
from time import gmtime, strftime
from bs4 import BeautifulSoup
from enum import Enum


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

# which BeautifulSoup parser to use
bsoup_parser = 'html5lib'

class def14aError(RuntimeError):
  pass

class def14aSection(Enum):
  NONE = 1
  ADDRESS = 2
  RESOLUTIONS = 3
  EVENTDATE = 4



class Edgarparser(object):
  """return structured data from html-rich EDGAR message"""
  logger = logging.getLogger(__name__)
  stdouthdlr = logging.StreamHandler(sys.stdout)
  stdouthdlr.setFormatter(logging.Formatter(LOGFORMAT))
  logger.addHandler(stdouthdlr)
  logger.setLevel(LOG_CURRENT_MINIMUM)



  ########################################################################################
  def stripHtmlTags(self, htmlTxt):
    """strip html tags from https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""
    try:
      if htmlTxt is None:
        return None
      else:
        return ''.join(BeautifulSoup(htmlTxt, bsoup_parser).findAll(text=True))
    except Exception as e:
      raise e.args[0]



  ########################################################################################
  def __parseevent(self, html):
    """parse the event-related elements
    date regexp from https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s04.html with extensions """
    try:
      # results storage
      eventdate = ""
      resolution = collections.OrderedDict()
      resolutionNumber = 0

      # define regular expressions for specific marker phrases
      re_eventdatestart = re.compile("time and date", re.IGNORECASE)
      # numeric date regexp
      date_regex1 = '(?:(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])|(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9]))/(?:[0-9]{2})?[0-9]{2}'
      # e.g. 10:00 a.m., Pacific Time, on Wednesday, November 14, 2019
      date_regex2 = '.*0?[0-9]{1}\:[0-9]{2}\s+[ap]{1}\.?[m]{1}.*[pacific|eastern|central|mountain].*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec].*[01]?[0-9]{1}.{1,2}2[0-9]{3}'
      re_eventdate = re.compile('(' + date_regex1 + '|' + date_regex2 + ')', re.IGNORECASE)
      re_address = re.compile("location|place", re.IGNORECASE)
      re_resolutions = re.compile("resolution|items of business", re.IGNORECASE)
      # optional bracket followed by some numbers then an optional bracket and/or and optional full stop
      match_resolution_number = "^\(?[0-9]+\)?\.?"
      # the resolution number plus at least one space plus some text
      match_whole_resolution = match_resolution_number + " +.+"
      re_oneresolution = re.compile(match_resolution_number)
      re_recorddate = re.compile("record date", re.IGNORECASE)
      re_signature = re.compile("by order of the board", re.IGNORECASE)

      # now we iterate over the text from the announcement onwards
      loop = 0 # indicative progress counter, just for debugging really

      whichSection = def14aSection.NONE

      # loop over the entire file from this point onwards
      while html != None:
        loop += 1
        # get the next element (when we start this, we have already "used" the first one to
        # find the meeting announcement start)
        html = html.next_element
        if html == None:
          break

        # cleanup the data we've found (convert to string, strip whitespace from the ends and
        # replace any embedded newlines with a space)
        lastitem = str(html).strip().replace('\n', ' ')

        # central processing switch
        #if len(lastitem) < 1:
        #  whichSection = def14aSection.NONE
        #  continue

        if str(html)[0] == '<':
          # ignore HTML
          continue
          self.logger.log(LOG_DEBUG, "CANDIDATE {0} {1}".format(loop, lastitem[:70]))

        elif whichSection == def14aSection.RESOLUTIONS:
          # add the found text to what we have already
          resolutionText = re.search('[a-zA-Z]+.*', lastitem)
          if resolutionText != None:
            resolutionText = resolutionText.group(0)
            self.logger.log(LOG_DEBUG, "found more text {0}".format(resolutionText))
            resolution[resolutionNumber] = resolution[resolutionNumber] + ' ' + resolutionText
            resolution[resolutionNumber] = resolution[resolutionNumber].strip()

        elif whichSection == def14aSection.EVENTDATE:
          self.logger.log(LOG_DEBUG, "CANDIDATE EVENT DATE {0} {1}".format(loop, lastitem[:70]))
          eventdate = re.search(re_eventdate, lastitem)
          if eventdate != None:
            whichSection = def14aSection.NONE # got it
            self.logger.log(LOG_DEBUG, "found meeting date {0} {1}".format(loop, eventdate.group(0)))

        elif re_eventdatestart.search(lastitem):
          whichSection = def14aSection.NONE
          eventdate = re.search(re_eventdate, lastitem)
          self.logger.log(LOG_DEBUG, "found meeting date? {0} {1}".format(loop, eventdate))
          if eventdate == None:
            whichSection = def14aSection.EVENTDATE # mark the fact that we are part-way through interpreting the event date
          self.logger.log(LOG_DEBUG, "found meeting date {0} {1}".format(loop, lastitem[:70]))

        elif re_resolutions.search(lastitem):
          whichSection = def14aSection.NONE
          self.logger.log(LOG_DEBUG, "found resolutions start {0} {1}".format(loop, lastitem[:70]))

        elif re_oneresolution.search(lastitem):
          self.logger.log(LOG_DEBUG, "found a resolution {0} {1}".format(loop, lastitem[:70]))
          whichSection = def14aSection.RESOLUTIONS
          resolutionNumber = re.search('[0-9]+', lastitem).group(0)
          resolution[resolutionNumber] = '' # start saving the resolution
          self.logger.log(LOG_DEBUG, "found a resolution number {0}".format(resolutionNumber))
          resolutionText = re.search('[a-zA-Z]+.*', lastitem)
          if resolutionText != None:
            resolution[resolutionNumber] = resolutionText.group(0)
            self.logger.log(LOG_DEBUG, "found text {0}".format(resolutionText.group(0)))
          else:
            whichSection == def14aSection.RESOLUTIONS

        elif re_recorddate.search(lastitem):
          whichSection = def14aSection.NONE
          self.logger.log(LOG_DEBUG, "found recorddate {0} {1}".format(loop, lastitem[:70]))

        elif re_signature.search(lastitem):
          whichSection = def14aSection.NONE
          self.logger.log(LOG_DEBUG, "found signature {0} {1}".format(loop, lastitem[:70]))

        # address has low priority; if other item "start texts" are found above, let them override
        elif whichSection == def14aSection.ADDRESS:
          self.logger.log(LOG_DEBUG, "found more address {0} {1}".format(loop, lastitem[:70]))

        elif re_address.search(lastitem):
          whichSection = def14aSection.ADDRESS
          self.logger.log(LOG_DEBUG, "found location {0} {1}".format(loop, lastitem[:70]))

        else:
          whichSection = def14aSection.NONE
          self.logger.log(LOG_DEBUG, "NOTHING {0} {1}".format(loop, lastitem[:70]))

    except Exception as e:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      self.logger.log(LOG_CRITICAL, "Abort during processing")
      self.logger.log(LOG_CRITICAL, sys.exc_info())
      imported_tb_info = traceback.extract_tb(exc_traceback)[-1]
      line_number = imported_tb_info[1]
      self.logger.log(LOG_CRITICAL, "at line number " + str(line_number))
      raise def14aError(e.args[0])


  ########################################################################################
  def def14a(self, html):
    """parse a def14a html message"""
    try:
      # init in case we can't find them or precursor
      meetingAnnouncement = ""
      meetingYear = ""

      self.logger.log(LOG_INFO, "Parsing started")

      soup = BeautifulSoup(html, bsoup_parser)
      # find the start of the meeting notice
      meetingAnnouncement = soup.find(string=re.compile("\Anotice.*of.*meeting.*of.*(stock|share)holders", re.DOTALL | re.IGNORECASE))
      if not meetingAnnouncement:
        raise def14aError("No meeting announcement line found")
      self.logger.log(LOG_DEBUG, "Meeting announcement found: {0}".format(meetingAnnouncement.strip()))

      # find the meeting year (exactly four digits starting with "2") within the herald text
      searchForMeetingYear = meetingAnnouncement
      while True:
        if str(searchForMeetingYear)[0] != '<':
          meetingYear = re.search("[12]{1}[0-9]{3}", searchForMeetingYear)
          if meetingYear != None:
            self.logger.log(LOG_DEBUG, "Meeting year found: {0}".format(meetingYear.group(0)))
            break
        # try the next element
        searchForMeetingYear = searchForMeetingYear.next_element
      if meetingYear == None:
        raise def14aError("No meeting year found")

      self.__parseevent(meetingAnnouncement)

      result = "".join(meetingAnnouncement), meetingYear

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