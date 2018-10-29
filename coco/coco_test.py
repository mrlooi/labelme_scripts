from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os.path as osp

def view_ann_mask(ann, img):
	m = coco.annToMask(ann)
	height, width, cn_ = img.shape

	mask = np.zeros((height, width), dtype=np.float32)
	# m = m.astype(np.float32) * cat_id
	mask[m>0] = m[m>0]

	# view mask
	mask_view = np.zeros((height, width, cn_), dtype=np.uint8)
	mask_view[m>0] = [255]*cn_ # set all pos to white color

	

	polys = np.array(ann['segmentation'][0], dtype=np.int32)  # x y x y
	polys = polys.reshape((np.size(polys)/2,2))
	img_copy = cv2.fillPoly(img, [polys], (0,255,0))

	mask_view = cv2.resize(mask_view, (960,540))
	cv2.imshow('mask', mask_view)
	cv2.imshow('img', cv2.resize(img_copy, (960,540)))
	cv2.waitKey(0)

# dataDir = '/home/vincent/hd/datasets/MSCOCO'
# dataType = 'val2014'
# imgDir = osp.join(dataDir, dataType)
# annFile = '{}/annotations/instances_{}.json'.format(dataDir,dataType)

labelme_root = "/home/vincent/LabelMe"
image_set = 'singulation_test'
annot_dir = osp.join(labelme_root, "Annotations", image_set)
imgDir = osp.join(labelme_root, "Images", image_set)
# annFile = "%s.json"%(image_set)
annFile = "%s.json"%("singulation_test_mini")

coco=COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['envelope']);
imgIds = coco.getImgIds(catIds=catIds );
img_d = coco.loadImgs(imgIds[np.random.randint(0,len(imgIds))])[0]

# img_path = osp.join(imgDir, img_d['file_name'])
# img = cv2.imread(img_path)
# cv2.imshow('img', img)
# cv2.waitKey(0)

annIds = coco.getAnnIds(imgIds=img_d['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
# coco.showAnns(anns)


for img_d in coco.loadImgs(imgIds):
	try:
		img_path = osp.join(imgDir, img_d['file_name'])
		img = cv2.imread(img_path)
		annIds = coco.getAnnIds(imgIds=img_d['id'], catIds=catIds, iscrowd=None)
		anns = coco.loadAnns(annIds)
		for ann in anns:
			view_ann_mask(ann, img)  #  binary mask
	except Exception, e:
		print("%s -> %s"%(e, img_d['file_name']))
