import scipy.io as sio
import xml.etree.ElementTree as ET
import argparse
import numpy as np

import glob
import os.path as osp
import os 
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-ad", "--annot_dir", required = True,
    help = "Annotation directory")
ap.add_argument("-id", "--image_dir", required = True,
    help = "Image directory")
args = vars(ap.parse_args())

annot_dir = args['annot_dir']
image_dir = args['image_dir']

annot_files = glob.glob(osp.join(annot_dir, '*.xml'))

for f in annot_files:
    tree = ET.parse(f)
    element = tree.getroot()
    objs = [e for e in element.findall('object') if int(e.find("deleted").text) != 1]
    h = int(element.find('imagesize').find('nrows').text)
    w = int(element.find('imagesize').find('ncols').text)

    f_basename = f[:f.rfind('.')].split("/")[-1]
    f_img = cv2.imread(osp.join(image_dir,f_basename + ".jpg"))
    img_h, img_w, _ = f_img.shape

    assert(img_h == h and img_w == w)

    # for e in objs:
        # if int(e.find("deleted").text) != 1:
            # classes[e.find('name').text.lower().strip()] = 1
            # break

            # e_poly = e.find('polygon')
            # e_pts = [( float(p.find('x').text), float(p.find('y').text) ) for p in e_poly.findall('pt')]
            # e_pts = np.array(e_pts, dtype=np.uint32)

            # p_max = np.amax(e_pts, axis=0)
            # p_min = np.amin(e_pts, axis=0)

            # x1 = max(p_min[0], 0)
            # y1 = max(p_min[1], 0)
            # x2 = min(p_max[0], w - 1)
            # y2 = min(p_max[1], h - 1)

            # assert(x2 <= w and y2 <= h)
