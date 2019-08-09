#  NOTE: In order to run this script, you must have the moss.pl file in the same diretory.
#        You can obtain this file by emailing moss@moss.stanford.edu with the following email content:
#               registeruser
#               email
#  NOTE: Before running this script, edit the codePost API key, courseName, and coursePeriod constants.
#
#  Usage: python3 sendToMoss.py <assignmentName> [-m] "[optional Moss arguments]"
#
#    <assignmentName> is the name of the assignment on codePost for which you want to assess code similarity
#
#    There are other moss arguments that you can pass in after -m (in quotes).
#    These can be seen in the moss.pl documentation or in the .README of this repo.
#
#    For example, you can run the following:
#       python3 sendToMoss.py assignmentName -m "-l java"
#    This will tell Moss that you are sending .java files. When Moss knows the language of the input code,
#       it will produce more accurate similarity scores.
#
#    This script does the following:
#       1. Gathers all the submissions of <assignmentName> and saves them in a temp directory,
#           in the format /tmp/<submissionID>_<students/*
#       2. Sends the submissions to Moss along with any optional Moss arguments provided.
#       3. Prints the Moss result link to the console.

import argparse
import codepost
import subprocess
import os
import shutil

#################### Constants -- PLEASE EDIT THESE ########################################
codepost.configure_api_key("<YOUR API KEY HERE>")
courseName="<YOUR CODEPOST COURSE NAME HERE>"
coursePeriod="<YOUR CODEPOST COURSE PERIOD HERE>"

##################### Argument Parsing ######################################################
parser = argparse.ArgumentParser(description='Working with Moss!')
parser.add_argument('assignmentName', help='Assignment Name')
parser.add_argument('-m','--m', nargs='*', help='Optional moss arguments')
args = parser.parse_args()

##################### Helper Functions ######################################################
# get the assignment from codePost based on the couseName, coursePeriod, and assignmentName
def getAssignment(courseName, coursePeriod, assignmentName):
    courses = list(codepost.course.list_available(name=courseName, period=coursePeriod))
    if len(courses) == 0:
        raise Exception("Course does not exist!")
    course = courses[0]

    assignments = [codepost.assignment.retrieve(id=a_id) for a_id in course.assignments]
    assignment = [a for a in assignments if a.name == assignmentName]
    if len(assignment) == 0:
        raise Exception("Assignment with name %s doesn't exist in %s | %s" % (assignmentName, courseName, coursePeriod))
    return assignment[0]

# Get all the submissions of the given assignment, and save them to a local temp folder
def getSubmissions(assignmentID):
    submissions = codepost.assignment.list_submissions(id=assignmentID)
    os.mkdir('tmp')
    for s in submissions:
        folderName = '{}_'.format(s.id) + ''.join(s.students)
        os.mkdir('tmp/{}'.format(folderName))
        for fID in s.files:
            f = codepost.file.retrieve(id=fID)
            file = open('tmp/{}/{}'.format(folderName,f.name), "w")
            file.write(f.code)
            file.close()

# Send the submissions to Moss
# If everything works correctly, a link will be outputted to the console
def runMossCheck():
    directories = [x[0]+'/*' for x in os.walk('./tmp') if x[0] != './tmp']
    if(args.m is not None):
        subprocess.call('./moss '+" ".join(args.m)+" -d "+" ".join(directories), shell=True)
    else:
        subprocess.call('./moss -d '+" ".join(directories), shell=True)


##################### Main  ######################################################
assignment = getAssignment(courseName, coursePeriod, args.assignmentName)
subs = getSubmissions(assignment.id)
try:
    runMossCheck()
    shutil.rmtree('./tmp') # delete tmp folder when complete
except:
    shutil.rmtree('./tmp') # delete tmp folder when complete
