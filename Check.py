import difflib

file1 = 'Dest.txt'
file2 = 'Note.txt'

diff = difflib.ndiff(open(file1).readlines(),open(file2).readlines())
re = ''.join(diff)
print(re)
print(type(re))
