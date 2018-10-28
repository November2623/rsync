import os, sys
stinfo = os.stat('Text.txt')
stinfo1 = os.stat('Dest.txt')

print(stinfo)
print('---------------------')
print(stinfo.st_atime)

print(stinfo.st_mtime)

print(stinfo1.st_atime)

print(stinfo1.st_mtime)