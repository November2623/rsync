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
    fsrc = open(filesrc,'r')
    lines     = fsrc.read()
    fsrc.close()
    fd = os.open(filedest, os.O_RDWR|os.O_CREAT )
    b = lines.encode()
    os.write(fd, b)
    os.close(fd)


def keep_permission(filesrc, filedest):
    stats = os.stat(filesrc)
    mark = ((stats.st_mode) |0o555) & 0o7775
    os.chmod(filedest, mark)

def keep_access_modification(filesrc, filedest):
    stinfo = os.stat(filesrc)
    atime = stinfo.st_atime
    mtime = stinfo.st_mtime
    os.utime(filedest,(atime, mtime))


def create_hardlink(filesrc, filedest):
    fd = os.open(filesrc, os.O_RDWR | os.O_CREAT)
    os.close(fd)
    os.link(filesrc, filedest)


def keep_symlink(filesrc, filedest):
    path = os.readlink(filesrc)
    if os.path.exists(filedest):
        if os.path.isdir(filedest):
            os.symlink(path, filedest+'/'+filesrc)
        elif os.path.isfile(filedest):
            os.unlink(filedest)
            os.symlink(path, filedest)
    else:
        if filedest[-1] == '/':
            os.mkdir(filedest[:-1])
            os.symlink(path, filedest + filesrc)
        else:
            os.symlink(path, filedest)



def check_file(filesrc, filedest):
    path = os.path
    if os.path.isfile(filesrc):
        if os.path.isdir(filedest):
            main(filesrc, filedest)
        else:
            main(filesrc, filedest)
    elif path.isdir(filesrc):
        print('skipping directory %s' % (filesrc))
    else:
        src_path = os.getcwd() + '/' + src_file_name
        print('rsync: link_stat %s failed: \
            No such file or directory (2)\
            \nrsync error: some files/attrs were not transferred (see previous errors)\
            (code 23) at main.c(1196) [sender=3.1.2]' % src_path)

def keep_hardlink(filesrc, filedest):
    if os.lstat(filesrc).st_nlink > 1:
        if os.path.isfile(filedest):
            os.unlink(filedest)
        os.link(filesrc, filedest)
        exit()
    elif os.path.islink(filesrc):
        keep_symlink(filesrc, filedest)
        exit()
def main(filesrc, filedest):
    keep_hardlink(filesrc, filedest)

check_file(file1, file2)
