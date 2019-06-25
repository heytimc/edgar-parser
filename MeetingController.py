""" Controller for the meeting """
from Meeting import Meeting
from DocumentRetriever import DocumentRetriever as dr
from bs4 import BeautifulSoup


class MeetingController():
    
    def __init__(self):
        self.meeting = Meeting()
        self.found_com_names = set()
        self.doc_retriever = dr()
        self.document_text = None
        self._found_links = None
        self._final_com_name = set()
        
    def updateView(self):
        return self.meeting.getAddress()
    
    def getMeetingData(self, search_term, start_date, end_date):
        self._getCompanyNames(search_term, start_date, end_date)
        
        if self.checkOnlyOneCompany(search_term):
            final_name = set(self._final_com_name)
            self._getDocumentTextLink()
            return final_name
        else:
            found_names = self.found_com_names
            self.found_com_names = set() # Reset the found com names for subsequent searches
            return found_names
        
    def checkOnlyOneCompany(self, searched_name):
        if not self.found_com_names: return False
        if len(self.found_com_names) > 1:
            for name in self.found_com_names:
                # An exact name for a company might get other hits
                # If the searched name is the exact name found then use this one
                if searched_name == name:
                    self._final_com_name.add(name)
                    return True
            # if there is no exact match then there is more than one company
            return False
        # Only one company found so all is fine
        self._final_com_name = self.found_com_names
        return True
    
    def _getCompanyNames(self, search_term, start_date, end_date):
        blacklist = ["[text]", "[html]"]
        doc_html = self.doc_retriever.getDocHTML(search_term, start_date, end_date)
        bs = BeautifulSoup(doc_html, 'html.parser')
        html_text = bs.prettify()
        
        self._found_links = bs.select("a[href*=Archives]")
        for link in self._found_links:
            if link.contents[0] not in blacklist:
                self.found_com_names.add(link.contents[0])
    
    def _getDocumentTextLink(self):
        company_name = self._final_com_name.pop()
        for link in self._found_links:
            if link.contents[0] == company_name:
                new_link = link.get('href').replace("-index.htm", ".txt")
                print(new_link)
        