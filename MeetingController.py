""" Controller for the meeting """
from Meeting import Meeting
from DocumentRetriever import DocumentRetriever as dr
from bs4 import BeautifulSoup

class MeetingController():
    
    def __init__(self):
        self.meeting = Meeting()
        self.found_com_names = set()
        self.doc_retriever = dr()
    def updateView(self):
        return self.meeting.getAddress()
    
    def getMeetingData(self, search_term, start_date, end_date):
        # Make calls to the model (Meeting Class)
        com_name = self._getActualCompanyName(search_term, start_date, end_date)
        for company in self.found_com_names:
            print(company)
    
    def _getActualCompanyName(self, search_term, start_date, end_date):
        blacklist = ["[text]", "[html]"]
        doc_html = self.doc_retriever.getDocHTML(search_term, start_date, end_date)
        bs = BeautifulSoup(doc_html, 'html.parser')
        html_text = bs.prettify()
        
        found_links = bs.select("a[href*=Archives]")
        for link in found_links:
            if link.contents[0] not in blacklist:
                self.found_com_names.add(link.contents[0])
    
    def _getDocumentTextLinks(self):
        pass