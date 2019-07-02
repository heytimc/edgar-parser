""" Module for the meeting view """
from bs4 import BeautifulSoup
import re
import datetime, logging, re, traceback, collections, sys
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

class Meeting(object):
    def __init__(self, meeting_data):
        self._address = None
        self._date = None
        self._resolution_data = None
        self.parser = BeautifulSoup(meeting_data, 'html.parser')
        self.logger = logging.getLogger(__name__)
        stdouthdlr = logging.StreamHandler(sys.stdout)
        stdouthdlr.setFormatter(logging.Formatter(LOGFORMAT))
        self.logger.addHandler(stdouthdlr)
        self.logger.setLevel(LOG_CURRENT_MINIMUM)

    def __parseevent(self, html):
        """parse the event-related elements"""
        try:
          # storage
          eventdate = ""
          resolution = collections.OrderedDict()
          resolutionNumber = 0
    
          # define regular expressions for specific marker phrases
          re_location = re.compile("location|place", re.IGNORECASE)
          re_resolutions = re.compile("resolution|items of business", re.IGNORECASE)
          # optional bracket followed by some numbers then an optional bracket and/or and optional full stop
          match_resolution_number = "^\(?[0-9]+\)?\.?"
          # the resolution number plus at least one space plus some text
          match_whole_resolution = match_resolution_number + " +.+"
          re_oneresolution = re.compile(match_resolution_number)
          re_recorddate = re.compile("record date", re.IGNORECASE)
          re_signature = re.compile("by order of the board", re.IGNORECASE)
    
          # now we iterate over the text from the herald onwards
          loop = 0 # indicative progress counter, just for debugging really
          inResolution = False # are we part-way through gathering a resolution's text?
    
          # loop over the entire file from this point onwards
          while html != None:
            loop += 1
            html = html.next_element
            if html == None:
              break
    
            # cleanup the data we've found (convert to string, strip whitespace from the ends and
            # replace any embedded newlines with a space)
            lastitem = str(html).strip().replace('\n', ' ')
    
            # central processing switch
            if len(lastitem) < 1:
              inResolution = False
    
            elif lastitem[0] == '<':
              # ignore HTML
              continue
              self.logger.log(LOG_DEBUG, "CANDIDATE {0} {1}".format(loop, lastitem[:70]))
    
            elif inResolution == True:
              # add the found text to what we have already
              resolutionText = re.search('[a-zA-Z]+.*', lastitem)
              if resolutionText != None:
                resolutionText = resolutionText.group(0)
                resolution[resolutionNumber] = resolution[resolutionNumber] + ' ' + resolutionText
                resolution[resolutionNumber] = resolution[resolutionNumber].strip()
                self.logger.log(LOG_DEBUG, "found more text {0}".format(resolutionText))
    
            elif re_location.search(lastitem):
              self.logger.log(LOG_DEBUG, "found location {0} {1}".format(loop, lastitem[:70]))
    
            elif re_resolutions.search(lastitem):
              self.logger.log(LOG_DEBUG, "found resolutions start {0} {1}".format(loop, lastitem[:70]))
    
            elif re_oneresolution.search(lastitem):
              self.logger.log(LOG_DEBUG, "found a resolution {0} {1}".format(loop, lastitem[:70]))
              inResolution = True
              resolutionNumber = re.search('[0-9]+', lastitem).group(0)
              resolution[resolutionNumber] = '' # start saving the resolution
              self.logger.log(LOG_DEBUG, "found a resolution number {0}".format(resolutionNumber))
              resolutionText = re.search('[a-zA-Z]+.*', lastitem)
              if resolutionText != None:
                resolution[resolutionNumber] = resolutionText
                self.logger.log(LOG_DEBUG, "found text {0}".format(resolutionText))
    
            elif re_recorddate.search(lastitem):
              self.logger.log(LOG_DEBUG, "found recorddate {0} {1}".format(loop, lastitem[:70]))
    
            elif re_signature.search(lastitem):
              self.logger.log(LOG_DEBUG, "found signature {0} {1}".format(loop, lastitem[:70]))
    
            else:
              self.logger.log(LOG_DEBUG, "NOTHING {0} {1}".format(loop, lastitem[:70]))
        except Exception as e:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          self.logger.log(LOG_CRITICAL, "Abort during processing")
          self.logger.log(LOG_CRITICAL, sys.exc_info())
          imported_tb_info = traceback.extract_tb(exc_traceback)[-1]
          line_number = imported_tb_info[1]
          self.logger.log(LOG_CRITICAL, "at line number " + str(line_number))
          raise def14aError(e.args[0])
    
    def getStuff(self):
        try:
          # init in case we can't find them or precursor
          meetingAnnouncement = ""
          meetingyear = ""
    
          self.logger.log(LOG_INFO, "Parsing started")
    
          # find the start of the meeting notice
          meetingAnnouncement = self.parser.find(string=re.compile("\Anotice.*of.*meeting.*of.*stockholders", re.DOTALL | re.IGNORECASE))
          if not meetingAnnouncement:
            raise def14aError("No meeting announcement line found")
    
          # find the meeting year (exactly four digits starting with "2") within the herald text
          self.logger.log(LOG_DEBUG, "Meeting announcement found: {0}".format(meetingAnnouncement.strip()))
          meetingyear = re.findall("2\d{3}", meetingAnnouncement)
          if not meetingyear:
            raise def14aError("No meeting year found")
    
          self.__parseevent(meetingAnnouncement)
    
          result = "".join(meetingAnnouncement), meetingyear
    
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
        
    
    def getAddress(self):
        return "Example Address\n"
    
    def getDate(self):
        pass
    
    def getText(self):
        pass
    
    def getInstructions(self):
        pass
