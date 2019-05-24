import requests
from bs4 import BeautifulSoup

com_name = input("Enter company name for DEF 14A search:")
response = requests.get("https://www.sec.gov/cgi-bin/srch-edgar?text=DEF+14A+{}&first=2019&last=2019".format(com_name))
   
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