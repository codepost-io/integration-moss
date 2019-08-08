# Moss-integration
This is a set of short scripts that can be used to connect [Moss](https://theory.stanford.edu/~aiken/moss/) with [codePost](https://codepost.io). Moss is a tool for assessing similarity between programs provided as an internet service by Stanford University and commonly used to detect instances of plagiarism in programming courses.

## 1. Sending Submissions From codePost to Moss:
Use `sendToMoss.py` to send the submissions corresponding to a single codePost assignment to Moss for processing. To do this, run

```
python3 sendToMoss.py <assignment name> [-m] "[optional Moss arguments]"
```

This script will print to the command line a link which contains the results produced by Moss.

Moss accepts the following optional arguments. 
* `-l language` - the source language of the tested programs
* `-d` - specifies that submissions are organized by directory, not by file
* `-b basefile_1 .... -b baefile_n` - names a "base file"
* `-m #` - sets the maximum number of times a given passage may appear before it is ignored
* `-c "string"` - comment string that will be attached to the report generated by Moss 

Some usage notes:
1. In order to run `sendToMoss.py`, you must have a `moss.pl` file in the directory from which the script is run. See the [Moss website](http://theory.stanford.edu/~aiken/moss/) or the `sendToMoss.py` file for instructions. 
2. Before running, you must edit the `codePost API Key`, `courseName`, and `coursePeriod` constants in `sendToMoss.py`. You can obtain your codePost API key [here](https://codepost.io/settings).
3. For the most accurate code similarity scores, use the `-l <language type>` optional parameter. For example,
  if you are comparing Java files for similarity, use the following `python3 sendToMoss.py <assignmentName> -m "-l java"`. See `moss.pl`
  for a full list of languages accepted by the `-l` parameter.

## 2. Processing Moss results to create codePost comments
After calculating Moss similarity scores using `sendToMoss.py`, the `processMossResults.py` script will allow you to place a codePost comment on each pair of codePost submissions `(sub1, sub2)` for which the similarity between `sub1` and `sub2` exceeds some threshold.

Run the script as follows. 

```
python3 processMossResults.py <MossURL> <threshold>
```

Some usage notes:
1. Before running, you must edit the `codePost API key` constant in `processMossResults.py`. 
2. This script assumes that the directories uploaded to Moss are in the format: `/tmp/<submissionID>_<student(s)>/<fileName>`. The `sendToMoss.py` script will automatically upload directories in this format, so if you used that script, you can ignore this instruction. But if you plan to use `processMossResults.py` independently of `sendToMoss.py`, then you'll want to modify `processMossResults.py` by editing the regexs used to parse Moss results to match your file names.
