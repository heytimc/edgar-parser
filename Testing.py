import requests
import re
from bs4 import BeautifulSoup
from PIL.JpegImagePlugin import COM

def getCompanyNames():
    response = requests.get("https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+electric&first=2019&last=2019")
    
    if response.status_code == 200:
        print("Success!")
    elif response.status_code == 404:
        print("Not found!")
    
    print("---COMPANY LIST---")
    print()
    text = response.content.decode("utf-8")
    
    bs = BeautifulSoup(text, 'html.parser')
    bs.prettify()
    
    blacklist = ["[text]", "[html]"]
    
    for link in bs.select("a[href*=Archives]"):
        if link.contents[0] not in blacklist: print(link.contents[0])

def getCompanyLinks():
    response = requests.get("https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+electric&first=2010&last=2019")
    
    if response.status_code == 200:
        print("Success!")
    elif response.status_code == 404:
        print("Not found!")
    
    print("---COMPANY LIST---")
    print()
    text = response.content.decode("utf-8")
    
    bs = BeautifulSoup(text, 'html.parser')
    bs.prettify()
    
    blacklist = ["[text]", "[html]"]
    
    for link in bs.select("a[href*=Archives]"):
        # print(link)
        if link.contents[0] == 'ALLEGHENY ENERGY, INC': 
            print(link.get('href'), link.contents[0])
        """
        if link.contents[0] == "[text]": 
            doclink = link.get('href')
        print(doclink)"""

# getCompanyLinks()



com_name = input("Enter a company name")
response = requests.get("https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+{}&first=2012&last=2019".format(com_name))
    
if response.status_code == 200:
    print("Success!")
elif response.status_code == 404:
    print("Not found!")
    
print("---COMPANY LIST---")
print()
text = response.content.decode("utf-8")
    
bs = BeautifulSoup(text, 'html.parser')
bs.prettify()
    
blacklist = ["[text]", "[html]"]
    
found_com_names = set()
links = bs.select("a[href*=Archives]")
for link in links:
    if link.contents[0] not in blacklist: 
        found_com_names.add(link.contents[0])

print("---These are the companies that were found for your search '{}'---".format(com_name))
# print(len(found_com_names))
choice_name_map  = {}
comnum = 1
for com in found_com_names:
    print(comnum, com) 
    choice_name_map[comnum] = com
    comnum +=1

print(choice_name_map)
final_chosen_com = choice_name_map[int(input("Enter choice"))]


document_text_files = []

#reg_exp = re.compile("^.*\-(.*)\-.*$")
for link in links:
    if link.contents[0] == final_chosen_com:
        new_link = link.get('href').replace("-index.htm", ".txt")
        print(new_link)
        print(str(new_link))
        print(re.findall('-\d+-', str(link)))
        





    