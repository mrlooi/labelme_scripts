import numpy as np
import cv2
import json
import os.path as osp
import xml.etree.ElementTree as ET
import copy
import datetime

def convert_datetime_to_string(dt=datetime.datetime.now(), formt="%Y-%m-%d %H:%M:%S"):
	return dt.strftime(formt)

class CocoAnnotationClass(object):
	def __init__(self, classes, supercategory=""):
		self.classes = classes
		self.map_classes_idx = {c: ix+1 for ix,c in enumerate(classes)}  # coco is 1-indexed
		self.map_idx_classes = {v:k for k,v in self.map_classes_idx.items()}
		self.data = self._get_default_data()
		for c,idx in self.map_classes_idx.items():
			self._add_category(c,idx,supercategory)

	def _get_default_data(self):
		default_d = {
			"info": {
				"year" : 2018, 
				"version" : "", 
				"description" : "", 
				"contributor" : "", 
				"url" : "", 
				"date_created" : convert_datetime_to_string()
			},
			"images": [],
			"annotations": [],
			"categories": [],
			"licenses": [
				{
					"id" : 1, 
					"name" : "", 
					"url" : ""
				}
			]
		}
		return default_d

	def set_classes(self, classes):
		self.classes = classes

	def clear(self):
		self.data = self._get_default_data()

	def _add_category(self, name, id=None, supercategory=""):
		cat_id = len(self.data["categories"]) + 1 if id is None else id
		cat_data = {
					"id" : cat_id, 
					"name" : name, 
					"supercategory" : supercategory
				}
		self.data["categories"].append(cat_data)

	def add_annot(self, id, img_id, img_cls, seg_data, is_crowd=0):
		"""ONLY SUPPORTS seg polygons of len 1 i.e. cannot support multiple polygons that refer to the same id"""
		if img_cls not in self.map_classes_idx:
			print("%s not in coco classes!"%(img_cls))
			return 
		cat_id = self.map_classes_idx[img_cls]
		seg_data_arr = np.array(seg_data)
		assert(len(seg_data_arr.shape) == 2)
		bbox = np.array([np.amin(seg_data_arr, axis=0), np.amax(seg_data_arr, axis=0)]).reshape(4)
		bbox[2:] -= bbox[:2]
		bbox = bbox.tolist()
		area = cv2.contourArea(seg_data_arr)
		annot_data =	{
					"id" : id,
					"image_id" : img_id,
					"category_id" : cat_id,
					"segmentation" : [seg_data_arr.flatten().tolist()],
					"area" : area,
					"bbox" : bbox,
					"iscrowd" : is_crowd
				}
		self.data["annotations"].append(annot_data)

	def add_image(self, id, width, height, file_name, date_captured=convert_datetime_to_string()):
		img_data =	{
					"id" : id,
					"width" : width,
					"height" : height,
					"file_name" : file_name,
					"license" : 1,
					"flickr_url" : "",
					"coco_url" : "",
					"date_captured" : date_captured
				}
		self.data["images"].append(img_data)

	def get_annot_json(self):
		return copy.deepcopy(self.data)


if __name__ == '__main__':
	import glob

	RED = (0,0,255)
	GREEN = (0,255,0)

	labelme_root = "/home/vincent/LabelMe"
	# labelme_root = "/home/drml/hd/datasets/LabelMe/"
	image_set = 'sm_data'
	# image_set = 'barcodes'
	coco_out_file = "%s.json"%(image_set)
	SUPERCATEGORY = 'loading' 
	CLASSES = ['box']#,'bar'] # ["barcode"]#,"box","envelope"]

	annot_dir = osp.join(labelme_root, "Annotations", image_set)
	img_dir = osp.join(labelme_root, "Images", image_set)
	assert osp.exists(img_dir) and osp.exists(annot_dir), "%s and/or %s does not exist!"%(img_dir, annot_dir)

	coco_annot = CocoAnnotationClass(CLASSES, SUPERCATEGORY)

	annot_dir_glob = glob.glob(annot_dir + "/*.xml")
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
		e_pts_all = []
		e_bboxes = []
		cnt = 0
		for e in element_objects:
			if int(e.find('deleted').text) == 1:
				continue
			# print(e.find('name').text)
			e_poly = e.find('polygon')
			e_cls = e.find('name').text
			e_pts = [( float(p.find('x').text), float(p.find('y').text) ) for p in e_poly.findall('pt')]
			e_pts = np.array(e_pts).astype(np.int32)
			e_bbox = np.array([np.amin(e_pts, axis=0), np.amax(e_pts, axis=0)]).reshape(4)
			e_bbox[2:] -= e_bbox[:2]
			e_pts_area = cv2.contourArea(e_pts)
			# print(e_cls)
			if e_cls not in CLASSES:
				continue
			# print("%s (%d), %.3f"%(e_cls, category_id, e_pts_area))
			e_bboxes.append(e_bbox)
			e_pts_all.append(e_pts)

			cnt += 1
			total_cnt += 1

			coco_annot.add_annot(total_cnt, IMG_ID, e_cls, e_pts)

			# img = cv2.imread(input_img_file)
			# img = cv2.rectangle(img, tuple(e_bbox[:2]), tuple(e_bbox[2:] + e_bbox[:2]), RED)
			# img = cv2.putText(img, e_cls, tuple(e_bbox[:2]), cv2.FONT_HERSHEY_COMPLEX, 0.6, GREEN)
			# img = cv2.fillPoly(img, [e_pts], GREEN)

			# cv2.imshow("img", img)
			# cv2.waitKey(0)

		if cnt == 0:
			continue

		coco_annot.add_image(IMG_ID, element_width, element_height, img_name)

		print("Parsed %d of %d: %s"%(IMG_ID, annot_dir_len, img_name))

	with open(coco_out_file, "w") as f:
		json.dump(coco_annot.get_annot_json(), f)
		print("Saved to %s"%(coco_out_file))
