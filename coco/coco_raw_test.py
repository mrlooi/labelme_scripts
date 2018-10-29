import numpy as np
import cv2
import json
import os.path as osp

RED = (0,0,255)
GREEN = (0,255,0)

dataDir='/home/vincent/hd/datasets/MSCOCO'
dataType='val2014'
imgDir = osp.join(dataDir, dataType)
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)
annFile = "val2014_mini.json"

# labelme_root = "/home/vincent/LabelMe"
# image_set = 'singulation_test' 
# annot_dir = osp.join(labelme_root, "Annotations", image_set)
# imgDir = osp.join(labelme_root, "Images", image_set)
# # annFile = "%s.json"%(image_set)
# annFile = "singulation_test_mini.json"

with open(annFile, 'r') as f:
	x = json.load(f)

categories = x['categories']

for ix,anno in enumerate(x['annotations']):
	ann_d = anno
	img_id = ann_d['image_id']
	for im_d in x['images']:
		if img_id == im_d['id']:
			img_d = im_d
			break
	img_name = img_d['file_name']
	img_path = osp.join(imgDir, img_name)

	img = cv2.imread(img_path)
	cv2.imshow("img", img)
	cv2.waitKey(0)

	ann_cat_id = ann_d['category_id']
	category = ""
	for c in categories:
		if ann_cat_id == c['id']:
			category = c['name']
			break

	bbox = np.array(ann_d['bbox'],dtype=np.int32)  # x y w h
	seg_data = ann_d['segmentation']
	if (len(seg_data) > 1):
		continue
	polys = np.array(seg_data, dtype=np.int32)  # x y x y
	polys = polys.reshape((np.size(polys)/2,2))

	print("Displaying annot %d"%(ix))

	img = cv2.rectangle(img, tuple(bbox[:2]), tuple(bbox[2:] + bbox[:2]), RED)
	img = cv2.putText(img, category, tuple(bbox[:2]), cv2.FONT_HERSHEY_COMPLEX, 0.6, GREEN)
	img = cv2.fillPoly(img, [polys], GREEN)
	cv2.imshow("img", img)
	cv2.waitKey(0)

