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


def new_data(dict_array, csv_path=f"{DOWNLOADS}/data.csv"):
    try:
        with open(csv_path, 'r') as csv_doc:
            csv_reader = csv.reader(csv_doc)

            written_pages = []
            for row in csv_reader:
                if row[0] != 'Page':
                    written_pages.append(row[0])

        new_entries = []
        for data in dict_array:
            if str(data['Page']) not in written_pages:
                new_entries.append(data)

        return new_entries
    except IOError:
        print('IOError occurred while reading csv file')


def append_row(dict_rows, csv_path=f"{DOWNLOADS}/data.csv"):
    try:
        with open(csv_path, 'a') as csv_doc:

            csv_writer = csv.DictWriter(csv_doc, fieldnames=COLUMN_NAMES)

            for data in dict_rows:
                csv_writer.writerow(data)

    except IOError:
        print('I/O Error occurred')


def parse(page_num, dict):
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
            dict['Page'] = page_num
            dict['Author'] = person_name

    # extract metadata about master thesis if thesis is open to view
    if has_access:
        # parse metadata
        labels = soup.find_all('td', {'class': 'metadataFieldLabel'})
        values = soup.find_all('td', {'class': 'metadataFieldValue'})

        for metadata in list(zip(labels, values)):
            label = metadata[0].get_text().replace(':', '').strip()
            value = metadata[-1].get_text().strip()
            dict[label] = value
            # print(f"{label} - {value}")

        # parse statistics
        for li in soup.find('div', {'id': 'statistics'}).ul.find_all('li'):
            label = ''.join(e.strip() for e in re.split(r'\d+', li.get_text()))
            value = li.span.get_text()
            dict[label] = value
            # print(f"{label} - {value}")

        # parse abstract
        abstract = soup.find('div', {'id': 'abstract'}).p.get_text()
        dict['Abstract'] = abstract
        # print(abstract)
        grouped_dicts.append(dict)
    else:
        print('failed to download thesis, falling back to next page')

    # iterate forward
    if page_num < 8500:
        parse(page_num+1, {})


if not os.path.exists(f"{DOWNLOADS}/data.csv"):
    create_file(f"{DOWNLOADS}/data.csv")
    try:
        with open(f"{DOWNLOADS}/data.csv", 'a') as doc:
            writer = csv.DictWriter(doc, fieldnames=COLUMN_NAMES)
            writer.writeheader()
    except IOError:
        print('I/O Error occurred')

grouped_dicts = []
parse(1100, {})
append_row(new_data(grouped_dicts))
