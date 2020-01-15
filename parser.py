from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import requests

# constants
DOWNLOADS = 'downloads'


def extract_name(soup):
    return soup.find('div', {'class': 'col-md-11'}).h5.strong.get_text()


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(path, url, mode='wb'):
    if not os.path.exists(path):
        open(path, mode).write(requests.get(url).content)


def create_file(path):
    if not os.path.exists(path):
        open(path, 'wra+')


def parse(page_num):
    page = urlopen(f"https://matheo.uliege.be/handle/2268.2/{page_num}")
    soup = BeautifulSoup(page, 'html.parser')
    has_access = False

    download_buttons = soup.find_all('a', {'class': 'btn btn-primary hidden-print'})
    file_names = soup.find_all('a', {'class': 'bitstream'})

    for link in list(zip(download_buttons, file_names)):
        if link[0].get_text() == 'View/Open':
            person_name = extract_name(soup)
            print(f"parsing page about {person_name}, page: {page}")

            # create named directory
            make_dir(f"{DOWNLOADS}/{person_name}")

            # download file (resume or thesis)
            download_file(f"{DOWNLOADS}/{person_name}/{link[-1].get_text()}", f"https://matheo.uliege.be/{link[-1].get('href')}")

            # mark to continue parsing
            has_access = True

    # extract metadata about master thesis if thesis is open to view
    if has_access:
        labels = soup.find_all('td', {'class': 'metadataFieldLabel'})
        values = soup.find_all('td', {'class': 'metadataFieldValue'})
        for metadata in list(zip(labels, values)):
            print(f"{metadata[0].get_text()} - {metadata[-1].get_text()}")

        create_file(f"{DOWNLOADS}/data.csv")
        with open(f"{DOWNLOADS}/data.csv", 'a') as doc:
            print(doc)
        #  fd.write(myCsvRow)
    else:
        print('failed to download thesis, falling back to next page')

    # iterate forward
    # if page_num < 7888:
    #     parse(page_num+1)


# make_dir(DOWNLOADS)
parse(6800)
