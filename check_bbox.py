import xml.etree.ElementTree as ET
import argparse

import glob
import numpy as np
import os.path as osp
import os 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required = True,
    help = "Annotation directory")
args = vars(ap.parse_args())


files = glob.glob(osp.join(args['dir'], '*.xml'))

CLASSES = ['box','envelope']

has_bbox_files = []

for f in files:
    tree = ET.parse(f)
    element = tree.getroot()
    objs = [e for e in element.findall('object') if int(e.find("deleted").text) != 1]

    has_bbox = False
    for ix, e in enumerate(objs):
        cls_name = e.find('name').text.lower().strip()
        if cls_name not in CLASSES:
            continue
        
        e_poly = e.find('polygon')
        e_pts = np.array([( float(p.find('x').text), float(p.find('y').text) ) for p in e_poly.findall('pt')], dtype=np.int32)

        # check if points are mere bounding boxes instead of masks
        # bounding box points are in the format: top_left, top_right, bottom_right, bottom_left
        if len(e_pts) == 4 and e_pts[0][1] == e_pts[1][1] and e_pts[0][0] == e_pts[3][0] and e_pts[2][1] == e_pts[3][1]:  # if top_left y and top_right y are the same
            has_bbox = True
            break

    if has_bbox:
        has_bbox_files.append(f.split("/")[-1].replace(".xml",""))

has_bbox_files = sorted(has_bbox_files)
print("***Files with bbox of %s:***\n"%(CLASSES))
print(has_bbox_files)
print("TOTAL: %d"%(len(has_bbox_files)))