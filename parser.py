from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
import os
import requests
import csv
import re
# constants
DOWNLOADS = 'downloads'
COLUMN_NAMES = ['Page', 'Title', 'Translated title', 'Date of defense', 'Advisor(s)', 'Rameau keyword(s)',
                "Committee's member(s)", 'Funders', 'Author', 'Language', 'Number of pages',
                'Keywords', 'Name of the research project', 'Research unit', 'Target public',
                'Discipline(s)', 'Institution(s)', 'Degree', 'Faculty', 'Commentary', 'Complementary URL',
                'Total number of views', 'Total number of downloads', 'Abstract']


def extract_name(soup):
    return soup.find('div', {'class': 'col-md-11'}).h5.strong.get_text()


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_file(path, url, mode='wb'):
    if not os.path.exists(path):
        open(path, mode).write(requests.get(url).content)


def create_file(path=f"{DOWNLOADS}/data-all-theses.csv"):
    if not os.path.exists(path):
        open(path, 'w+')


def new_data(dict_array, csv_path=f"{DOWNLOADS}/data-all-theses.csv"):
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


def append_row(dict_rows, csv_path=f"{DOWNLOADS}/data-all-theses.csv"):
    try:
        with open(csv_path, 'a') as csv_doc:

            csv_writer = csv.DictWriter(csv_doc, fieldnames=COLUMN_NAMES)

            for data in dict_rows:
                try:
                    csv_writer.writerow(data)
                except ValueError as e:
                    print('ValueError')
                    print(e)

    except IOError:
        print('I/O Error occurred')


def parse(page_num, dict):
    try:
        page = urlopen(f"https://matheo.uliege.be/handle/2268.2/{page_num}")
    except URLError:
        print("Something went wrong. falling back to the next page")
        return

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
        abstract = soup.find('div', {'id': 'abstract'}).p
        if abstract is not None:
            dict['Abstract'] = abstract.get_text()

        grouped_dicts.append(dict)
    else:
        print('failed to download thesis, falling back to next page')
        # iterate forward


def parse_to_csv(page_num, dict):
    print(page_num)
    try:
        page = urlopen(f"https://matheo.uliege.be/handle/2268.2/{page_num}")
    except URLError as e:
        print("Something went wrong. falling back to the next page")
        print(e)
        return

    soup = BeautifulSoup(page, 'html.parser')
    try:
        person_name = extract_name(soup)
    except:
        print('no data')
        return False

    dict['Page'] = page_num
    dict['Author'] = person_name

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
    abstract = soup.find('div', {'id': 'abstract'}).p
    if abstract is not None:
        dict['Abstract'] = abstract.get_text()

    grouped_dicts.append(dict)
    append_row(new_data([dict]))


def iterate_recursive(page_num):
    if page_num < 8500:
        parse(page_num, {})
        iterate_recursive(page_num+1)


def iterate(page_num):
    while page_num <= 8500:
        parse(page_num, {})
        page_num += 1


def iterate_csv_only(page_num=1):
    with open(f"{DOWNLOADS}/data-all-theses.csv", 'r') as csv_doc:
        csv_reader = csv.reader(csv_doc)

        written_pages = []
        for row in csv_reader:
            if row[0] != 'Page':
                written_pages.append(row[0])
        print(written_pages)
    while page_num <= 9000:
        if str(page_num) not in written_pages:
            parse_to_csv(page_num, {})
        page_num += 1


if not os.path.exists(f"{DOWNLOADS}/data-all-theses.csv"):
    create_file(f"{DOWNLOADS}/data-all-theses.csv")
    try:
        with open(f"{DOWNLOADS}/data-all-theses.csv", 'a') as doc:
            writer = csv.DictWriter(doc, fieldnames=COLUMN_NAMES)
            writer.writeheader()
    except IOError:
        print('I/O Error occurred')

# counter = 0
grouped_dicts = []
# iterate(1113)
# append_row(new_data(grouped_dicts))
iterate_csv_only()
