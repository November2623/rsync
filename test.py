# Python Difflib demo
# Author: Neal Walters
# loosely based on http://ahlawat.net/wordpress/?p=371
# 01/17/2011

# build the files here - later we will just read the files probably
file1Contents="""
for j = 1 to 10:
   print "ABC"
   print "DEF"
   print "HIJ"
   print "JKL"
   print "Hello World"
   print "j=" + j
   print "XYZ"
"""

file2Contents = """
for j = 1 to 10:
   print "ABC"
   print "DEF"
   print "HIJ"
   print "JKL"
   print "Hello World"
   print "XYZ"
print "The end"
"""

filename1 = "diff_file1.txt"
filename2 = "diff_file2.txt"

file1 = open(filename1,"w")
file2 = open(filename2,"w")

file1.write(file1Contents)
file2.write(file2Contents)

file1.close()
file2.close()
#end of file build

lines1 = open(filename1, "r").readlines()
lines2 = open(filename2, "r").readlines()

import difflib


diffSequence = difflib.ndiff(lines1, lines2)

print("\n ----- SHOW DIFF ----- \n")
for i, line in enumerate(diffSequence):
    if line[0] == '-':
        line.split('-')
        print(line)

# diffObj = difflib.Differ()
# deltaSequence = diffObj.compare(lines1, lines2)
# deltaList = list(deltaSequence)
#
# print("\n ----- SHOW DELTALIST ----- \n")
# for i, line in enumerate(deltaList):
#     print(line)
#
# #let's suppose we store just the diffSequence in the database
# #then we want to take the current file (file2) and recreate the original (file1) from it
# #by backward applying the diff
#
# contextDiffSeq = difflib.context_diff(lines1, lines2)
# contextDiffList = list(contextDiffSeq)
#
# for i, line in enumerate(contextDiffList):
#     print (line)
