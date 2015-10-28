from sys import argv
import time
import csv
import os


TIMESTAMP = time.strftime('%H%M-%Y%m%d')

class Article():
    fulltxt = ""
    Title = ""
    Publication = ""
    Date = ""
    Year = ""
    Author = ""
    PQID = ""

CSVNAME = os.path.abspath('Documents/Scratch/ProQuestToPlainText_' + TIMESTAMP + '.csv')
FIELDS = ['PQID', 'Title', 'Author', 'Publication', 'Date', 'Year']
csv_file = open(CSVNAME, 'wb')
csvwriter = csv.DictWriter(csv_file, delimiter=',', fieldnames=FIELDS)

#write csv headers
csvwriter.writerow(dict((fn, fn) for fn in FIELDS))

def abbreviate(pub):
    """returns a publication abbreviation to be included in the filename of the textfile"""
    pubs = {
        'USA TODAY (pre-1997 Fulltext)' : 'USAT',
        'USA TODAY' : 'USAT',
        'New York Times' : 'NYT',
        'Wall Street Journal' : 'WSJ'
    }
    return pubs.get(pub, "X")

def write_metadata(doc):
    """write the field values of the current doc to the csv file"""
    if doc.fulltxt != "":
        writefields = dict((field, getattr(doc, field)) for field in vars(doc) if not field.startswith('__') and field != 'fulltxt')
        csvwriter.writerow(writefields)

def write_article(doc):
    """write the full text of the article to it's own text file."""
    DOCNAME = abbreviate(doc.Publication) + '_' + doc.Year + '_' + doc.PQID + '.txt'
    name = os.path.abspath('Documents/Scratch/'+DOCNAME)
    with open(name, 'a') as f:
        f.write(doc.Title)
        f.write(doc.fulltxt)


script, filename = argv
docs = open(filename)
readingtxt = False

for line in docs:
    line = line.strip()
    if line == "____________________________________________________________":
        #write out the previous doc
        try: doc
        except NameError: doc = None
        else:
            write_article(doc)
            write_metadata(doc)
        #start new doc
        doc = Article()
        continue
    if line.startswith("Full text:"):
    	 #we're reading the full text
         readingtxt = True
         doc.fulltxt = line.split("Full text: ")[1]
         continue
    elif readingtxt:
    	 if line.startswith("Illustration") or line == "" :
    	 	readingtxt = False
    	 	continue
    	 else:
    	 	doc.fulltxt = doc.fulltxt + "\n" + line
    elif line.startswith("Title: "):
         doc.Title = line.split("Title: ")[1]
    elif line.startswith("Publication title: "):
         Publication = line.split("Publication title: ")[1]
         doc.Publication = Publication.split(",")[0]
    elif line.startswith("Author: "):
         doc.Author = line.split("Author: ")[1]
    elif line.startswith("Publication date: "):
         doc.Date = line.split("Publication date: ")[1]
    elif line.startswith("ProQuest document ID: "):
         doc.PQID = line.split("ProQuest document ID: ")[1]
    elif line.startswith("Publication year: "):
         doc.Year = line.split("Publication year: ")[1]
    elif not line or line.isspace() :
         continue
    else:
         continue

csv_file.close()
docs.close()