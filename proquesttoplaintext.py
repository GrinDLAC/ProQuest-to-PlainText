from sys import argv
import time
import csv

TIMESTAMP = time.strftime('%H%M-%Y%m%d')

class Article():
    fulltxt = ""
    Title = ""
    Publication = ""
    Date = ""
    Year = ""
    Author = ""
    PQID = ""

CSVNAME = 'ProQuestToPlainText_' + TIMESTAMP + '.csv'
FIELDS = ['PQID', 'Title', 'Author', 'Publication', 'Date', 'Year']
csvFile = open(csvName, 'wb')
csvwriter = csv.DictWriter(csvFile, delimiter=',', fieldnames=fields)

#write csv headers
csvwriter.writerow(dict((fn, fn) for fn in fields))

def abbreviate(pub):
    #a publication abbreviation is included in the filename of the textfile
    pubs = {
        'USA TODAY (pre-1997 Fulltext)' : 'USAT',
        'USA TODAY' : 'USAT',
        'New York Times' : 'NYT',
        'Wall Street Journal' : 'WSJ'
    }
    return pubs.get(pub, "X")

def writeMetadata(doc):
    #write the field values of the current doc to the csv file
    if doc.fulltxt != "":
        writefields = dict((field, getattr(doc, field)) for field in vars(doc) if not field.startswith('__') and field != 'fulltxt')
        csvwriter.writerow(writefields)

def writeArticle(doc):
    name = abbreviate(doc.Publication)+'_'+doc.Year+'_'+doc.PQID+'.txt'
    with open(name, 'a') as f:
        f.write(doc.Title)
        f.write(doc.fulltxt)


script, filename = argv
docs = open(filename)
readingtxt = False

for line in docs:
    line = line.strip()
    if line == '____________________________________________________________':
        #write out the previous doc
        try: doc
        except NameError: doc = None
        else:
            writeArticle(doc)
            writeMetadata(doc)
        #start new doc
        doc = Article()
        continue
    if line.startswith("Full text:"):
    	 #we're reading the full text
         readingtxt = True
         doc.fulltxt = line[10:]
         continue
    elif readingtxt:
    	 if line.startswith("Illustration") or line == "" :
    	 	readingtxt = False
    	 	continue
    	 else:
    	 	doc.fulltxt = doc.fulltxt + "\n" +line
    elif line.startswith("Title: "):
         doc.Title = line.split("Title: ")[1]
    elif line.startswith("Publication title: "):
         doc.Publication = line.split("Publication title: ")[1]
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

csvFile.close()
docs.close()