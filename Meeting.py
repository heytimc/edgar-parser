""" Module for the meeting view """
from Edgarparser import Edgarparser

class Meeting(object):
    def __init__(self, meeting_data):
        self._address = None
        self._date = None
        self._resolution_data = None
        self._meeting_data = meeting_data
        self.parser = Edgarparser()
        
    def getData(self):
        return self.parser.def14a(self._meeting_data)
