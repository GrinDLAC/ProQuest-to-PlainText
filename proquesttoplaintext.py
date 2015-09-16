from sys import argv
import time
import csv

timestamp = time.strftime('%H%M-%Y%m%d')

class Article(object):
    fulltxt = ""
    Title = ""
    Publication = ""
    Date = ""
    Year = ""
    Author = ""
    PQID = ""

csvName = 'ProQuestToPlainText_'+timestamp+'.csv'
fields = ['PQID', 'Title', 'Author', 'Publication', 'Date', 'Year']
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
    txtFile = open(name, 'a')
    txtFile.write(Article.fulltxt)
    txtFile.close()


script, filename = argv
docs = open(filename)
readingtxt = False

for line in docs:
    line = line.strip()
    if line == '____________________________________________________________':
        #write out the previous doc
        writeArticle(Article)
        writeMetadata(Article)
        #start new doc
        doc = Article()
        continue
    if line.startswith("Full text:"):
    	 #we're reading the full text
         readingtxt = True
         Article.fulltxt = line[10:]
         continue
    elif readingtxt:
    	 if line.startswith("Illustration") or line == "" :
    	 	readingtxt = False
    	 	continue
    	 else:
    	 	Article.fulltxt = Article.fulltxt + "\n" +line
    elif line.startswith("Title:"):
         Article.Title = line[6:]
    elif line.startswith("Publication title:"):
         Article.Publication = line[19:]
    elif line.startswith("Author:"):
         Article.Author = line[8:]
    elif line.startswith("Publication date:"):
         Article.Date = line[18:]
    elif line.startswith("ProQuest document ID:"):
         Article.PQID = line[22:]
    elif line.startswith("Publication year:"):
         Article.Year = line[18:]
    elif not line or line.isspace() :
         continue
    else:
         continue

csvFile.close()
docs.close()