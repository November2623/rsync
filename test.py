#!/usr/bin/python3
import argparse, os, os.path
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


def create_symlink(filesrc, filedest):
    os.symlink(filesrc, filedest)


def create_hardlink(filesrc, filedest):
    fd = os.open(filesrc, os.O_RDWR|os.O_CREAT)
    os.close(fd)
    os.link(filesrc, filedest)


def is_hardlink(file):
    temp = os.stat(file).st_nlink
    if temp == 1:
        return True
    return False

def symlink(filesrc, filedest):
    if os.path.islink(filesrc):
        path = os.readlink(filesrc)
        if os.path.exists(filedest):
            if os.path.isdir(filedest):
                os.symlink(filesrc, path + '/' + filedest)
            elif os.path.isfile(filedest):
                os.unlink(filedest)
                os.symlink(filesrc, filedest)


symlink(file1, file2)
