# Moss-integration
This is a set of short scripts to use Moss with codePost. Moss is a fantastic tool to check code similarity among submissions.

## 1. Sending Submissions From codePost to Moss:
Usage: `python3 sendToMoss.py assignmentName [-m] "[optional Moss arguments]"`
      - This gets all the codePost submissions for `assignmentName` and sends it to Moss
      - Optional parameters provided are passed into Moss processing
The link to the MOSS result will be printed to the command line

Notes:
1. In order to run this, you must have the `moss.pl` file in your directory when this is run. See website http://theory.stanford.edu/~aiken/moss/ or the `sendToMoss.py` file for instructions. 
2. Before running, set the variables for `codePost API Key`, `courseName`, and `coursePeriod`
3. For the best code similarity calculations, pass in the -l <language type> parameter as arguments. For example,
  if your files are java, you would do the following `python3 sendToMoss.py assignmentName -m "-l java"`. See `moss.pl`
  for a full list of the languages supported by Moss. 

## 2. Processing MOSS results and creating comments on codePost
Usage: `python3 processMossResults.py MossURL threshold"`
      - This gets the results at the MossURL, and creates an comment on every pair of submissions `(sub1, sub2)` where:
            `codeSimilarity(sub1, sub2) >= threshold`
Notes:
1. This script assumes that the directories uploaded to Moss are of the format: `/tmp/<submissionID>_<student(s)>/<fileName>`.
   If you're using this to process the results from `sendToMoss.py`, then you don't have to worry about this. 
   But if you plan to use this script separately, then you'll want to modify `processMossResults.py` to edit the regex
   matching to meet your file name. 
