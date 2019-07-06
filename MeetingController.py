# Author: Harry Pearson
# Email: harry.pearson@student.anglia.ac.uk
# Date: 28/06/2019
from numpy.core.numeric import full

""" Controller for the meeting """
from Meeting import Meeting
from DocumentRetriever import DocumentRetriever as dr
from bs4 import BeautifulSoup
import re
import requests

class MeetingController():
    
    def __init__(self):
        self.found_com_names = set()
        self.doc_retriever = dr()
        self._found_links = None
        self._final_com_name = set()
        self._document_data = {}
        
    def updateView(self):
        return self.meeting.getAddress()
    
    def getDocumentParts(self):
        resolutions = []
        for doc_number in self._document_data:
            for doc in self._document_data[doc_number]:
                meeting_data = self._document_data[doc_number][doc]
                meeting = Meeting(meeting_data)
                resolutions.append(meeting.getStuff())
                # print(len(self._document_data[doc_number][doc]))
        return resolutions
        
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
        link="https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+{0}&first={1}&last={2}".format(search_term, start_date, end_date)
        doc_html = self.doc_retriever.getDocHTML(link)
        bs = BeautifulSoup(doc_html, 'html.parser')
        html_text = bs.prettify()
        
        self._found_links = bs.select("a[href*=Archives]")
        for link in self._found_links:
            if link.contents[0] not in blacklist:
                self.found_com_names.add(link.contents[0])
    
    def _getDocumentTextLink(self):
        company_name = self._final_com_name.pop()
        document_links = []
        for link in self._found_links:
            if link.contents[0] == company_name:
                new_link = link.get('href').replace("-index.htm", ".txt")
                document_links.append(new_link)
        
        self._storeDocumentText(document_links)
        
    def _storeDocumentText(self, document_links):
        base_url = "https://www.sec.gov"
        documents = {}
        document_number = 1
        for text_link in document_links:
            full_link = base_url+text_link
            print(full_link)
            year = re.findall("-\d+-", full_link)[0].strip('-')
            if int(year) >= 00 and int(year) <= 94:
                document_year = "20"+year
            elif int(year) >= 94:
                document_year = "19"+year
            
            text = self.doc_retriever.getDocHTML(full_link)
            document = {document_year: text}
            documents[document_number] = document
            document_number += 1
        
        self._document_data = documents
