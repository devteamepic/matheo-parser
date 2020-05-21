import csv
import docx

with open(f"downloads/data-all-theses.csv", 'r') as csv_doc:
    csv_reader = csv.reader(csv_doc)

    authors = []
    for row in csv_reader:
        if row[0] != 'Page':
            authors.append([row[1], row[8]])

print(len(authors))

doc = docx.Document()

table = doc.add_table(rows=len(authors)+1, cols=2)

table.style = 'Table Grid'
row = table.rows[0]
row.cells[0].text = "Authors"
row.cells[1].text = "Titles"

for i, author in enumerate(authors):
    print(i, author[1])
    row = table.rows[i+1]
    row.cells[0].text = author[1]
    row.cells[1].text = author[0]

doc.save("downloads/authors.docx")