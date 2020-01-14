from urllib.request import urlopen
from bs4 import BeautifulSoup

page = urlopen("https://matheo.uliege.be/handle/2268.2/6800")

soup = BeautifulSoup(page, 'html.parser')

# print(soup.find_all('a', {'class': 'btn btn-primary hidden-print'}))

for link in soup.find_all('a', {'class': 'btn btn-primary hidden-print'}):
    print(link.get('href'), link.get_text())