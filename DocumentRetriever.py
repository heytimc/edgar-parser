""" Class for retrieving the DEF-14A document """
from abc import ABC, abstractmethod
import requests
from builtins import staticmethod
from _codecs import decode

class DocumentRetriever():
    def __init__(self):
        self._base_url = "https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+{0}&first={1}&last={2}"
        # self._document_url = doc_url
        self._document_text = None
    
    def getDocHTML(self, com_name, start_date, end_date):
        response = requests.get("https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+{0}&first={1}&last={2}".format(com_name, 
                                                                                                                    start_date, 
                                                                                                                    end_date))
        if response.status_code == 200:
            print("Success!")
        elif response.status_code == 404:
            print("Not found!")
        html_text = self.decode_response(response)
        return html_text
    
    def decode_response(self, response):
        return response.content.decode("utf-8")
