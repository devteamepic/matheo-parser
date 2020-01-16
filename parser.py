from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import requests
import csv
import re
# constants
DOWNLOADS = 'downloads'
COLUMN_NAMES = ['Page', 'Title', 'Translated title', 'Date of defense', 'Advisor(s)',
                "Committee's member(s)", 'Funders', 'Author', 'Language', 'Number of pages',
                'Keywords', 'Target public', 'Discipline(s)', 'Institution(s)', 'Degree', 'Faculty',
                'Total number of views', 'Total number of downloads', 'Abstract']


def extract_name(soup):
    return soup.find('div', {'class': 'col-md-11'}).h5.strong.get_text()


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(path, url, mode='wb'):
    if not os.path.exists(path):
        open(path, mode).write(requests.get(url).content)


def create_file(path=f"{DOWNLOADS}/data.csv"):
    if not os.path.exists(path):
        open(path, 'w+')


def append_row(dict_rows, csv_path=f"{DOWNLOADS}/data.csv"):
    try:
        with open(csv_path, 'a') as csv_doc:
            csv_writer = csv.DictWriter(csv_doc, fieldnames=COLUMN_NAMES)

            for data in dict_rows:
                csv_writer.writerow(data)

    except IOError:
        print('I/O Error occurred')


def parse(page_num):
    page = urlopen(f"https://matheo.uliege.be/handle/2268.2/{page_num}")
    soup = BeautifulSoup(page, 'html.parser')
    has_access = False

    download_buttons = soup.find_all('a', {'class': 'btn btn-primary hidden-print'})
    file_names = soup.find_all('a', {'class': 'bitstream'})

    for link in list(zip(download_buttons, file_names)):
        if link[0].get_text() == 'View/Open':
            person_name = extract_name(soup)
            print(f"parsing page about {person_name}, page: {page_num}")

            # create named directory
            make_dir(f"{DOWNLOADS}/{person_name}")

            # download file (resume or thesis)
            download_file(f"{DOWNLOADS}/{person_name}/{link[-1].get_text()}", f"https://matheo.uliege.be/{link[-1].get('href')}")

            # mark to continue parsing
            has_access = True

    # extract metadata about master thesis if thesis is open to view
    if has_access:
        # parse metadata
        labels = soup.find_all('td', {'class': 'metadataFieldLabel'})
        values = soup.find_all('td', {'class': 'metadataFieldValue'})
        for metadata in list(zip(labels, values)):
            print(f"{metadata[0].get_text().strip()} - {metadata[-1].get_text().strip()}")

        # parse statistics
        for li in soup.find('div', {'id': 'statistics'}).ul.find_all('li'):
            print(''.join(e.strip() for e in re.split(r'\d+', li.get_text())), li.span.get_text())

        # parse abstract
        print(soup.find('div', {'id': 'abstract'}).p.get_text())
    else:
        print('failed to download thesis, falling back to next page')

    # iterate forward
    # if page_num < 7888:
    #     parse(page_num+1)


if not os.path.exists(f"{DOWNLOADS}/data.csv"):
    create_file(f"{DOWNLOADS}/data.csv")
    try:
        with open(f"{DOWNLOADS}/data.csv", 'a') as doc:
            writer = csv.DictWriter(doc, fieldnames=COLUMN_NAMES)
            writer.writeheader()
    except IOError:
        print('I/O Error occurred')
parse(1815)
