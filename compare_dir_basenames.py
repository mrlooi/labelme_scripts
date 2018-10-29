import argparse
import glob
import os.path as osp

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d1", "--dir1", required = True,
	help = "Directory 1")
ap.add_argument("-d2", "--dir2", required = True,
	help = "Directory 2")
args = vars(ap.parse_args())

d1_files = [f[:f.rfind('.')].split("/")[-1] for f in glob.glob(osp.join(args["dir1"],"*"))]
d2_files = [f[:f.rfind('.')].split("/")[-1] for f in glob.glob(osp.join(args["dir2"],"*"))]

files_not_in_d2 = [f for f in d1_files if f not in d2_files]

print(files_not_in_d2)
