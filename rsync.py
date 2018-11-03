#!/usr/bin/python3
import argparse
import os
import os.path
import hashlib
from stat import *


parser = argparse.ArgumentParser()
parser.add_argument('file1', help = 'srcfile')
parser.add_argument('file2', help = 'destfile')
parser.add_argument('-c', '--checksum', action = 'store_true')
parser.add_argument('-u', '--update', action = 'store_true')
args = parser.parse_args()
file1 = args.file1
file2 = args.file2


def check_sum(filesrc, filedest):
	hasher1 = hashlib.md5()
	afile1 = open(filesrc, 'rb')
	buf1 = afile1.read()
	a = hasher1.update(buf1)
	md5_a = str(hasher1.hexdigest())

	hasher2 = hashlib.md5()
	afile2 = open(filedest, 'rb')
	buf2 = afile2.read()
	b = hasher2.update(buf2)
	md5_b = str(hasher2.hexdigest())
	return md5_a == md5_b


def check_time(filesrc, filedest):
	src_atime = os.stat(filesrc).st_atime
	src_mtime =os.stat(filesrc).st_mtime
	dest_atime = os.stat(filedest).st_atime
	dest_mtime = os.stat(filedest).st_mtime
	return src_atime == dest_atime and src_mtime == dest_mtime


def check_size(filesrc, filedest):
	src_size = os.stat(filesrc).st_size
	dest_size = os.stat(filedest).st_size
	return src_size == dest_size


def check_size_of_file(filesrc, filedest):
	src_size = os.stat(filesrc).st_size
	dest_size = os.stat(filedest).st_size
	if src_size < dest_size:
		copy_content(filesrc, filedest)
	else:
		update_content(filesrc, filedest)

def check_update(filesrc, filedest):
	dest_mtime = os.stat(filedest).st_mtime
	src_mtime = os.stat(filesrc).st_mtime
	if dest_mtime > src_mtime:
		exit()
	elif dest_mtime == src_mtime:
		return check_sum(filesrc, filedest)
	else:
		return False


def check_option(args, filesrc, filedest):
	if os.path.isfile(filesrc):
		if args.checksum:
			return check_sum(filesrc, filedest)
		elif args.update:
			return check_update(filesrc, filedest)
		else:
			return check_size(filesrc, filedest) and check_time(filesrc, filedest)
	else:
		return False


def keep_permission(filesrc, filedest):
	get_mod = os.stat(filesrc).st_mode
	os.chmod(filedest, get_mod)


def keep_time(filesrc, filedest):
	src_atime = os.stat(filesrc).st_atime
	src_mtime = os.stat(filesrc).st_mtime
	os.utime(filedest, (src_atime, src_mtime))


def update_content(filesrc, filedest):
	file1 = os.open(filesrc, os.O_RDONLY)
	src_content = os.read(file1, os.path.getsize(filesrc))
	file2 = os.open(filedest, os.O_RDWR | os.O_CREAT)
	dest_content = os.read(file2, os.path.getsize(filedest))
	count = 0
	while count < os.path.getsize(filesrc):
		os.lseek(file1, count ,0)
		os.lseek(file2, count, 0)
		if count < len(dest_content):
			if dest_content[count] != src_content[count]:
				os.write(file2, os.read(file1, 1))
		else:
			os.write(file2, os.read(file1, 1))
		count += 1


def copy_content(filesrc, filedest):
    fsrc = open(filesrc, 'r')
    lines = fsrc.read()
    fsrc.close()
    fd = os.open(filedest, os.O_RDWR | os.O_CREAT)
    b = lines.encode()
    os.write(fd, b)
    os.close(fd)


def file_scr_normal(filesrc, filedest):
	if os.path.exists(filedest):
		if os.path.isfile(filedest):
			if os.lstat(filedest).st_nlink > 1:
				os.unlink(filedest)
				copy_content(filesrc, filedest)
			elif os.path.islink(filedest):
				os.unlink(filedest)
				copy_content(filesrc, filedest)
			else:
				check_size_of_file(filesrc, filedest)
		elif os.path.isdir(filedest):
			update_content(filesrc, os.path.join(filedest, filesrc))
	else:
		if filedest[-1] == '/':
			os.mkdir(filedest[:-1])
			copy_content(filesrc, os.path.join(filedest, filesrc))
		else:
			copy_content(filesrc, filedest)


def file_scr_symlink(filesrc, filedest):
	path = os.readlink(filesrc)
	if os.path.exists(filedest):
		if os.path.isfile(filedest):
			os.unlink(filedest)
			os.symlink(path, filedest)
		elif os.path.isdir(filedest):
			os.symlink(path, filedest + '/' + filesrc)
	else:
		if filedest[-1] == '/':
			os.mkdir(filedest[:-1])
			os.symlink(path, filedest + filesrc)
		else:
			os.symlink(path, filedest)



def file_src_hardlink(filesrc, filedest):
	if os.path.exists(filesrc):
		if os.path.isfile(filedest):
			os.unlink(filedest)
			os.link(filesrc, filedest)
		elif os.path.isdir(filedest):
			os.link(filesrc, filedest + '/' + filesrc)
	else:
		if filedest[-1] == '/':
			os.mkdir(filedest[:-1])
			os.link(filesrc, filedest + filesrc)
		else:
			os.link(filesrc, filedest)

def check(filesrc, filedest):
	if os.path.exists(filesrc):
		if os.path.isfile(filesrc):
			main(filesrc, filedest)
		elif os.path.isdir(filesrc):
			print('skipping directory %s' %(filesrc))
	else:
		print("rsync: link_stat \"" + os.path.abspath(filesrc) + "\"" +
             " failed: No such file or directory (2)")
def main(filesrc, filedest):
	try:
		a = 0
		src_file = os.open(filesrc, os.O_RDONLY)
		a = 1 
		# dest_file = os.open(filedest, os.O_RDWR | os.O_CREAT)
		if os.path.exists(filedest):
			if check_option(args, filesrc, filedest):
				exit()
			else:
				if os.lstat(filesrc).st_nlink > 1:
					file_src_hardlink(filesrc, filedest)
				elif os.path.islink(filesrc):
					file_scr_symlink(filesrc, filedest)
				else:
					file_scr_normal(filesrc, filedest)
				keep_permission(filesrc, filedest)
				keep_time(filesrc, filedest)
		else:
		
			if os.lstat(filesrc).st_nlink > 1:
				if filedest[-1] == '/':
					os.mkdir(filedest[:-1])
					os.link(filesrc, filedest + filesrc)
				else:
					os.link(filesrc, filedest)
	
			elif os.path.islink(filesrc):
				if filedest[-1] == '/':
					os.mkdir(filedest[:-1])
					os.symlink(path, filedest + filesrc)
				else:
					os.symlink(path, filedest)
			else:
				if filedest[-1] == '/':
					os.mkdir(filedest[:-1])
					copy_content(filesrc, os.path.join(filedest, filesrc))
				else:
					copy_content(filesrc, filedest)
			keep_permission(filesrc, filedest)
			keep_time(filesrc, filedest)


	except PermissionError:
		if a == 0:
			# path = os.getcwd() + '/' + filesrc
			print("rsync: send_files failed to open \"" + os.path.abspath(filesrc) +
             "\"" + ": Permission denied (13)")
		else:
			# path = os.getcwd() + '/' +filedest
			print("rsync: send_files failed to open \"" + os.path.abspath(filedest) +
             "\"" + ": Permission denied (13)")

if __name__ == '__main__':
	check(file1, file2)