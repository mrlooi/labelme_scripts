import xml.etree.ElementTree as ET
import argparse

import glob
import os.path as osp
import os 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required = True,
    help = "Annotation directory")
args = vars(ap.parse_args())


files = glob.glob(osp.join(args['dir'], '*.xml'))

DELETED_THRESH = 3

empty_annots = []
delete_thresh_annots = []
classes = {}
for f in files:
    tree = ET.parse(f)
    element = tree.getroot()
    objs = [e for e in element.findall('object') if int(e.find("deleted").text) != 1]

    # check if empty
    if len(objs) == 0:
        empty_annots.append(f)

    # get classes from annot
    for e in objs:
        classes[e.find('name').text.lower().strip()] = 1
            # break

    # check number of deleted
    deletes = len(element.findall('object')) - len(objs)
    if deletes >= DELETED_THRESH:
        delete_thresh_annots.append(f)

print("Total files %d"%len(files))
print("All classes: %s"%(classes.keys()))
print("Files with empty annots: %s"%empty_annots)
# print("Files with annots >= deleted thresh of %d: TOTAL (%d) \n\t%s"%(DELETED_THRESH, len(delete_thresh_annots), delete_thresh_annots))
print("Files with annots >= deleted thresh of %d: TOTAL (%d)"%(DELETED_THRESH, len(delete_thresh_annots)))