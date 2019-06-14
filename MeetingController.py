""" Controller for the meeting """
from Meeting import Meeting

class MeetingController():
    
    def __init__(self):
        self.meeting = Meeting()
    
    def updateView(self):
        return self.meeting.getAddress()