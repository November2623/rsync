import os.path
def islink():
    if os.path.islink('File2'):
        return True
    return False
print(islink())
