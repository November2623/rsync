import argparse, os


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
    lines = fsrc.read()
    fsrc.close()
    fd = os.open(filedest, os.O_RDWR|os.O_CREAT )
    b = lines.encode()
    os.write(fd, b)
    os.close(fd)

Copy_file(file1,file2)
