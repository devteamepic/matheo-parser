import csv

# with open(f"downloads/data.csv", 'r') as csv_doc:
#     csv_reader = csv.reader(csv_doc)
#
#     written_pages = []
#     for row in csv_reader:
#         if row[0] != 'Page':
#             written_pages.append(row[0])
#
# print(written_pages)

with open(f"downloads/data.csv", 'r') as csv_doc:
    csv_reader = csv.reader(csv_doc)
    for row in csv_reader:
        print(row[23], len(row))