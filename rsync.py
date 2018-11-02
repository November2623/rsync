#!/usr/bin/python3
import argparse
import os
import os.path
from stat import *

parser = argparse.ArgumentParser()

parser.add_argument('file1',help='srcfile')
parser.add_argument('file2',help='destfile')
parser.add_argument('-c', '--checksum', action='store_true')
parser.add_argument('-u', '--update', action='store_true')
args = parser.parse_args()
file1 = args.file1
file2 = args.file2


def check_sum(filesrc, filedest):
    md5_src = hashlib.md5(filesrc).hexdigest()
    md5_dest = hashlib.md5(filedest).hexdigest()
    return md5_src == md5_dest


def Copy_file(filesrc, filedest):
    fsrc = open(filesrc,'r')
    lines = fsrc.read()
    fsrc.close()
    fd = os.open(filedest, os.O_RDWR|os.O_CREAT )
    b = lines.encode()
    os.write(fd, b)
    os.close(fd)

def check_time(filesrc, filedest):
    src_access_time = os.stat(filesrc).st_atime
    src_modification_time = os.stat(filesrc).st_mtime
    dest_access_time = os.stat(filedest).st_atime
    dest_modification_time = os.stat(filedest).st_mtime
    return src_access_time == dest_access_time and src_modification_time == dest_modification_time


def check_update(filesrc, filedest):
    dest_mod_time = os.stat(filedest).st_mtime
    src_mod_time = os.stat(filesrc).st_mtime
    if dest_mod_time > src_mod_time:
        exit()
    elif dest_mod_time == src_mod_time:
        return check_sum(filesrc, filedest)
    else:
        return False


def check_size(filesrc, filedest):
    src_size = os.stat(filesrc).st_size
    dest_size =os.stat(filedest).st_size
    return src_size == dest_size


def check_option(args, filesrc, filedest):
    if os.path.isfile(filesrc) and os.path.isfile(filedest):
        if args.checksum:
            return check_sum(filesrc, filedest)
        elif args.update:
            return check_update(filesrc, filedest)
        else:
            return check_size(filesrc, filedest) and check_time(filesrc, filedest):
    else:
        return False


def keep_permission(filesrc, filedest):
    stats = os.stat(filesrc)
    mark = ((stats.st_mode) | 0o555) & 0o7775
    os.chmod(filedest, mark)

def keep_access_modification(filesrc, filedest):
    stinfo = os.stat(filesrc)
    atime = stinfo.st_atimecheck_option()
    mtime = stinfo.st_mtime
    os.utime(filedest,(atime, mtime))

#
# def create_hardlink(filesrc, filedest):
#     fd = os.open(filesrc, os.O_RDWR | os.O_CREAT)
#     os.close(fd)
#     os.link(filesrc, filedest)

#
# def keep_symlink(filesrc, filedest):
#     path = os.readlink(filesrc)
#     if os.path.exists(filedest):
#         if os.path.isdir(filedest):
#             os.symlink(path, filedest+'/'+filesrc)
#         elif os.path.isfile(filedest):
#             os.unlink(filedest)
#             os.symlink(path, filedest)
#     else:
#         if filedest[-1] == '/':
#             os.mkdir(filedest[:-1])
#             os.symlink(path, filedest + filesrc)
#         else:
#             os.symlink(path, filedest)


def keep_symlink_hardlink(filesrc, filedest):
    if os.lstat(filesrc).st_nlink > 1:
        if os.path.exists(filedest):                        #Check hardlink file_src
            if os.path.isdir(filedest):
                os.link(filesrc, filedest+'/'+filesrc)
            elif os.path.isfile(filedest):
                os.unlink(filedest)
                os.link(filesrc, filedest)
        else:
            if filedest[-1] == '/':
                os.mkdir(filedest[:-1])
                os.link(filesrc, filedest + filesrc)
            else:
                os.link(filesrc, filedest)
    elif os.path.islink(filesrc):                           # Check symlink file_src
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
    else:
        if os.path.exists(filedest):
            if os.path.isfile(filedest):
                if os.lstat(filedest).st_nlink > 1:
                    unlink(filedest)
                elif os.islink(filedest):
                    unlink(filedest)
            elif os.path.isdir(filedest):
                Copy_file(filesrc, os.path.join(filedest, filesrc))
        else:
            if filedest[-1] == '/':
                os.mkdir(filedest[:-1])
                Copy_file(filesrc, os.path.join(filedest, filesrc))
            else:
                Copy_file(filesrc, filedest)


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


# def keep_hardlink(filesrc, filedest):
#     if os.lstat(filesrc).st_nlink > 1:
#         if os.path.isfile(filedest):
#             os.unlink(filedest)
#             os.link(filesrc, filedest)
#         else:
#             os.link(filesrc, filedest + filesrc)
#     elif os.path.islink(filesrc):
#         keep_symlink(filesrc, filedest)

def main(filesrc, filedest):
    try:
        a = 0
        scr_file = os.open(filesrc, os.O_RDONLY)
        a = 1
        dest_file = os.open(filedest, os.O_RDWR | os.O_CREAT)
        if check_option(args, filesrc, filedest):
            exit()
        else:
            keep_symlink_hardlink(filesrc, filedest)
    except PermissionError:
        if a == 0:
            path = os.getcwd() + '/'/ + filesrc
        else:
            path = os.getcwd() + '/' + filedest
        print('rsync: send_files failed to open "%s":\
        Permission denied (13)\
        \nrsync error: some files/attrs were not transferred\
        (see previous errors) (code 23) at main.c(1183) [sender=3.1.1]' % path)
        exit()
