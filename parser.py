from urllib.request import urlopen
from bs4 import BeautifulSoup
# print(soup.find_all('a', {'class': 'btn btn-primary hidden-print'}))


def parse(page_num):
    page = urlopen(f"https://matheo.uliege.be/handle/2268.2/{page_num}")
    soup = BeautifulSoup(page, 'html.parser')

    for link in soup.find_all('a', {'class': 'btn btn-primary hidden-print'}):
        if link.get_text() == 'View/Open':
            print(link.get('href'), link.get_text())
            # create directory, download file
        else:
            # break execution of current page
            print('restricted/forbidden')
            return

    # extract metadata about master thesis

    for metadata in list(zip(soup.find_all('td', {'class': 'metadataFieldLabel'}),
                             soup.find_all('td', {'class': 'metadataFieldValue'}))):
        print(f"{metadata[0].get_text()} - {metadata[-1].get_text()}")
    # if page_num < 7888:
    #     parse(page_num+1)


parse(1814)
