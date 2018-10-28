import argparse, os
from stat import *

parser = argparse.ArgumentParser()

parser.add_argument('file1',help='srcfile')
parser.add_argument('file2',help='destfile')
args = parser.parse_args()
file1 = args.file1
file2 = args.file2


def Copy_file(filesrc, filedest):

    # with open(file1) as f:
    #     with open(file2) as f1:
    #         for line in f:
    #             f1.write(line)

    fsrc = open(filesrc,'r')
    lines     = fsrc.read()
    fsrc.close()
    fd = os.open(filedest, os.O_RDWR|os.O_CREAT )
    b = lines.encode()
    os.write(fd, b)
    os.close(fd)


def fix_permission(filesrc, filedest):
    stats = os.stat(filesrc)
    mark = ((stats.st_mode) |0o555) & 0o7775
    os.chmod(filedest, mark)

def fix_access_modification(filesrc, filedest):
    stinfo = os.stat(filesrc)
    atime = stinfo.st_atime
    mtime = stinfo.st_mtime
    os.utime(filedest,(atime, mtime))

fix_access_modification(file1, file2)
