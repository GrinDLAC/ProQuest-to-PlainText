from sys import argv
import time
import csv

timestamp = time.strftime('%H%M-%Y%m%d')

class Article(object):
    fulltxt = ""
    Title = ""
    Publication = ""
    Date = ""
    PQID = ""

csvName = 'ProQuestToPlainText_'+timestamp+'.csv'
fields = ['PQID', 'Title', 'Publication', 'Date']
csvFile = open(csvName, 'wb')
csvwriter = csv.DictWriter(csvFile, delimiter=',', fieldnames=fields)
#write csv headers
csvwriter.writerow(dict((fn, fn) for fn in fields))

def writeMetadata(doc):
    #write the field values of the current doc to the csv file
    if doc.fulltxt != "":
        writefields = dict((field, getattr(doc, field)) for field in vars(doc) if not field.startswith('__') and field != 'fulltxt')
        csvwriter.writerow(writefields)

def writeArticle(doc):
    name = doc.PQID+'.txt'
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
    elif line.startswith("Publication date:"):
         Article.Date = line[18:]
    elif line.startswith("ProQuest document ID:"):
         Article.PQID = line[22:]
    elif not line or line.isspace() :
         continue
    else:
         continue

csvFile.close()
docs.close()