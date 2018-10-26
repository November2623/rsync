import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--files', required=True, nargs='+')

args = parser.parse_args()

print(args.files)
