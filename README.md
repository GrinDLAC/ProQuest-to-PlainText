# ProQuest-to-PlainText
This small program was created to facilitate textual analysis of articles from three publications that are available through the ProQuest database, The New York Times, The Wall Street Journal, and USA Today.  The program can be adapted to process any file exported from ProQuest using the process described here.

First you'll need to generate a text file that includes the full text of articles returned from a search on ProQuest's database. You'll need to have access to ProQuest through your institution.
  > Once you have access to ProQuest, perform a search and request only documents that contain full-text.
  > Export the results in batches (as large as you're comfortable with) to a plain text file
  > Run the ProQuest-to-PlainText script on the text file downloaded from ProQuest.  (There is a sample ProQuest plain text file included in this repository so you can confirm that the file you downloaded matches the format that the script expects.  If it doesn't, it won't work.)
  > The script will produce a single CSV file containing the metadata for all the documents that were included in the processed file and an individual text file containing the full text for each document.  If you downloaded 200 documents from ProQuest into a single file you'll get 1 CSV of the metadata and 200 text files of the full text (each named with the ProQuest Document ID)