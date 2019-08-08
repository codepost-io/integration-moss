#  Usage: python3 processMossResults.py MossURL threshold
#
#  NOTE: This script only works if the files uploaded to Moss are of the format
#        '/tmp/<submissionID>_<student(s)>/<fileName>'
#
#  This script takes a Moss URL and a similarity threshold for which to report plagiarism and:
#     1. Gets the results from the <Moss URL>, which compares items with the syntax:
#           '/tmp/<submissionID>_<student(s)>/<fileName>'
#     2. Processes the results to find the set of (submissionID1, submissionID2, similarity) tuples
#        for which similarity >= threshold
#     3. Adds a comment to the first files of submissionID1 and submissionID2 with a comment to
#       flag that the similarity between submission1 and submission2 exceeded the specified threshold

import pandas as pd
import re
import argparse
import codepost

codepost.configure_api_key("<YOUR API KEY HERE>")

##################### Argument Parsing ######################################################
parser = argparse.ArgumentParser(description='Working with Moss!')

# argument parser for similarity thresholds
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

parser.add_argument('mossURL', help='URL of Moss Results')
parser.add_argument('threshold', type=restricted_float, help='A percentage similarity threshold. e.g., 50% = .5')

args = parser.parse_args()

##################### Process Moss results  ######################################################
# Get results from a mossURL and output tutples of (submissionID1, submissionID2, similarity)
def readResults(mossURL, threshold):
    dfs = pd.read_html(mossURL, header=0)
    similarSubmissions = []
    for index, row in dfs[0].iterrows():
        similarity = re.search(r'(?<=\()(\d*?)(?=%)', row['File 1']).group()
        submissionID1 = re.search(r'(?<=/)(\d*?)(?=_)', row['File 1']).group()
        submissionID2 = re.search(r'(?<=/)(\d*?)(?=_)', row['File 2']).group()
        if(float(similarity)/100 >= threshold):
            similarSubmissions.append((submissionID1, submissionID2, similarity))
    return similarSubmissions

def addComment(submissionID1, submissionID2, similarity):
    """
    Adds comments to the first file of a submission, noting that there was plagiarism detected in this submission
    """
    sub = codepost.submission.retrieve(id=int(submissionID1))  # get the student's submission
    fileID = sub.files[0]    # get the id of the first file from the submissions

    # create a comment on the first file of that submission
    my_comment = codepost.comment.create(
      text="FLAG: High level of code similarity with another submission. {}% similarity with submission id {}".format(similarity, submissionID2),
      startChar=1,
      endChar=1,
      startLine=1,
      endLine=2,
      file=fileID,
      pointDelta=0,
      rubricComment=None)

    print("Comment added to submission. Visit the URL here to view: codepost.io/code/{}".format(submissionID1))

##################### Main  ######################################################
similarResults = readResults(args.mossURL, args.threshold)
for (submissionID1, submissionID2, similarity) in similarResults:
    addComment(submissionID1, submissionID2, similarity)
    addComment(submissionID2, submissionID1, similarity)
