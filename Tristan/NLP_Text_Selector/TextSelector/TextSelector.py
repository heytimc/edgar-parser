import re
import requests
from bs4 import BeautifulSoup

htmlPage = requests.get("https://www.sec.gov/Archives/edgar/data/1504678/000147793219002566/llpp_def14a.htm")
fourteenA = BeautifulSoup(htmlPage.content, 'html.parser')

#keyWord = re.compile("meeting", re.IGNORECASE)
#possibleMeetings = fourteenA.find_all(string=keyWord)
#for meeting in possibleMeetings:
#    print(meeting)
#    print("\n")
#    pass

actionNumberRegex = "^\(?[0-9]+\)?\.?"
possibleAction = fourteenA.find_all(valign="top")
listOfActions = []
addNextWord = False;
for action in possibleAction:
    if addNextWord == True:
        addNextWord = False
        listOfActions.append(action.prettify())
        pass
    if action.find(string=re.compile(actionNumberRegex)):
        addNextWord = True;
        listOfActions.append(action.prettify())
        pass
    pass

for action in listOfActions:
    print(action)
    print("\n")
    pass
