# MOSS-integration
This is a set of short scripts to use MOSS with codePost. MOSS is a fantastic open source tool to check code similarity among submissions.

## 1. Sending Submissions From codePost to Moss:
Usage: `python3 sendToMoss.py assignmentName [-m] "[optional Moss arguments]"`
      - This gets all the codePost submissions for `assignmentName` and sends it to MOSS
      - Optional parameters provided are passed into MOSS processing
The link to the MOSS result will be printed to the command line

Notes:
1. In order to run this, you must have the `moss.pl` file in your directory when this is run. See website http://theory.stanford.edu/~aiken/moss/ or the `sendToMoss.py` file for instructions. 
2. Before running, set the variables for `codePost API Key`, `courseName`, and `coursePeriod`
3. For the best code similarity calculations, pass in the -l <language type> parameter as arguments. For example,
  if your files are java, you would do the following `python3 sendToMoss.py assignmentName -m "-l java"`. See `moss.pl`
  for a full list of the languages supported by Moss. 

## 2. Sending Submissions From codePost to Moss:
Usage: `python3 sendToMoss.py assignmentName [-m] "[optional Moss arguments]"`
