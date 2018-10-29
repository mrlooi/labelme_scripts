# Aditya's Script
import argparse

import glob
import os.path as osp
import os 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ad", "--annot_dir", required = True,
    help = "Annotation directory")
ap.add_argument("-id", "--image_dir", required = True,
    help = "Image directory")
args = vars(ap.parse_args())

annot_dir = args['annot_dir']
image_dir = args['image_dir']

remove_extension = lambda x: x[:x.find(".")]

annotations = set(map(remove_extension, os.listdir(annot_dir)))
images = set(map(remove_extension, os.listdir(image_dir)))

images_not_annotated = images - annotations
missing_annotated_images = annotations - images


print "Images that has not been annotated: ", len(images_not_annotated)
for i in images_not_annotated:
	print i
print "=================================="
print "Images that is missing but annotatation is found: ", len(missing_annotated_images)
for i in missing_annotated_images:
	print i
print "=================================="

