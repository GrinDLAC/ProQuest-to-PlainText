# ProQuest-to-PlainText
This small program was created to facilitate textual analysis of articles from three publications that are available through the ProQuest database, The New York Times, The Wall Street Journal, and USA Today.  The program can be adapted to process any file exported from ProQuest using the process described here. This document reflects the process as used in September of 2015.  Mileage may vary if ProQuest makes changes.

First you'll need to generate a text file that includes the full text of articles returned from a search on ProQuest's database. You'll need to have access to ProQuest through your institution.

1. Once you have access to ProQuest, perform a search and request only documents that contain full-text.

2. Export the results in batches (as large as you're comfortable with) to a plain text file.  Select the articles to export then click "...More" and select "Text Only".  In the Export/Save pane Output should be set to "Text Only" and Content should be set to "Full text (citation, abstract, full text, images, indexing".  Uncheck the boxes in the Include section (Recent Searches, Table of contents, Cover page/header, Document numbering)

3. Run the ProQuest-to-PlainText script on the text file downloaded from ProQuest.  (There is a sample ProQuest plain text file included in this repository so you can confirm that the file you downloaded matches the format that the script expects.  If it doesn't, it won't work.)

4. The script will produce a single CSV file containing metadata for all the documents that were included in the processed file and an individual text file containing the full text for each document.  If you downloaded 200 documents from ProQuest into a single file you'll get 1 CSV of the metadata and 200 text files of the full text.  Included in the csv are the ProQuest document ID, Title, Author, Publication, Date of Publication, and Publication Year.  The full text files contain the Title and the full text and the filename includes a publication abbreviation, publication year, and the ProQuest document ID. For example: NYT_2006_306802422.txt