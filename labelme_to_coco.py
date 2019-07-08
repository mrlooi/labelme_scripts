import numpy as np
import cv2
import json
import os.path as osp
import xml.etree.ElementTree as ET
import copy
import datetime

from collections import defaultdict 

from coco_annotation import CocoAnnotationClass

def recursively_get_all_subchild_ids(e_id, element_ids_dict):
	if e_id not in element_ids_dict:
		return []

	e = element_ids_dict[e_id]

	parts = e.find("parts")
	# CHECK CHILD
	child_parts = parts.find("hasparts").text
	all_child_ids = []
	if child_parts and len(child_parts) > 0:
		child_ids = [cid for cid in child_parts.split(",") if cid != e_id]
		all_child_ids += child_ids
		for cid in child_ids:
			all_child_ids += recursively_get_all_subchild_ids(cid, element_ids_dict)

	return all_child_ids

def find_top_parent_id(e_id, element_ids_dict):
	if e_id not in element_ids_dict:
		return None
	e = element_ids_dict[e_id]

	parts = e.find("parts")
	# CHECK PARENT
	parent = parts.find("ispartof").text
	if parent and len(parent) > 0 and parent != e_id:
		upper_parent = find_top_parent_id(parent, element_ids_dict)
		if upper_parent and len(upper_parent) > 0 and upper_parent not in [parent, e_id]:
			parent = upper_parent
	else:
		parent = e_id
	return parent

if __name__ == '__main__':
	import glob
	from natsort import natsorted

	RED = (0,0,255)
	GREEN = (0,255,0)

	VIS = True

	labelme_root = "/home/bot/LabelMe"
	# labelme_root = "/home/drml/hd/datasets/LabelMe/"
	image_set = 'pen_dataset'
	# image_set = 'barcodes'
	coco_out_file = "%s.json"%(image_set)
	SUPERCATEGORY = 'pen_dataset' #'unloading' 
	CLASSES = ['pen', 'pencil'] #['box'] # ["barcode"]#,"box","envelope"]

	annot_dir = osp.join(labelme_root, "Annotations", image_set)
	img_dir = osp.join(labelme_root, "Images", image_set)
	assert osp.exists(img_dir) and osp.exists(annot_dir), "%s and/or %s does not exist!"%(img_dir, annot_dir)

	coco_annot = CocoAnnotationClass(CLASSES, SUPERCATEGORY)

	annot_dir_glob = natsorted(glob.glob(annot_dir + "/*.xml"))[17:18]

	annot_dir_len = len(annot_dir_glob)
	total_cnt = 0
	for ix, annot_file in enumerate(annot_dir_glob):
		# input_annot_file = glob.glob(annot_dir + "/*.xml")[0]
		file_basename = annot_file.split("/")[-1].replace(".xml","")
		img_name = file_basename + ".jpg"
		input_img_file = osp.join(img_dir, img_name)
		
		IMG_ID = ix + 1

		et = ET.parse(annot_file)
		element = et.getroot()
		element_file = element.find('filename')
		element_img_sz = element.find('imagesize')
		
		element_height = int(element_img_sz.find('nrows').text)
		element_width = int(element_img_sz.find('ncols').text)
		print("Element height %d, width %d"%(element_height, element_width))

		element_objects = element.findall('object')
		
		parent_child_ids = defaultdict(list)
		element_ids = {}

		cnt = 0
		for e in element_objects:
			# print(e.find('name').text)
			if int(e.find('deleted').text) == 1:
				continue
			e_id = e.find("id").text
			element_ids[e_id] = e

		used_ids = []
		for e_id in element_ids:

			parent_id = find_top_parent_id(e_id, element_ids)
			child_ids = recursively_get_all_subchild_ids(parent_id, element_ids)
			all_ids = list(set(child_ids + [parent_id]))

			valid_ids = [id for id in all_ids if id not in used_ids and id in element_ids]
			if len(valid_ids) == 0:
				continue
			# print(all_ids)
			used_ids += valid_ids

			polygons = []
			for id in valid_ids:
				e = element_ids[id]
				e_cls = e.find('name').text
				if e_cls not in CLASSES:
					continue
				
				e_poly = e.find('polygon')
				e_pts = [( float(p.find('x').text), float(p.find('y').text) ) for p in e_poly.findall('pt')]
				e_pts = np.array(e_pts).astype(np.int32)
				polygons.append(e_pts)

			if len(polygons) == 0:
				continue

			cnt += 1
			total_cnt += 1

			coco_annot.add_annot(total_cnt, IMG_ID, e_cls, polygons)

			if VIS:
				img = cv2.imread(input_img_file)
				for poly in polygons:
					# img = cv2.rectangle(img, tuple(e_bbox[:2]), tuple(e_bbox[2:] + e_bbox[:2]), RED)
					# img = cv2.putText(img, e_cls, tuple(e_bbox[:2]), cv2.FONT_HERSHEY_COMPLEX, 0.6, GREEN)
					img = cv2.fillPoly(img, [poly], GREEN)

				ih, iw = img.shape[:2]
				if ih > 960 or iw > 960:
					img = cv2.resize(img, (960, 960))
				cv2.imshow("img", img)
				cv2.waitKey(0)

		if cnt == 0:
			continue

		coco_annot.add_image(IMG_ID, element_width, element_height, img_name)

		print("Parsed %d of %d: %s"%(IMG_ID, annot_dir_len, img_name))

	with open(coco_out_file, "w") as f:
		json.dump(coco_annot.get_annot_json(), f)
		print("Saved to %s"%(coco_out_file))
