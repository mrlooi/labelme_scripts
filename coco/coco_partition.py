import json
import os.path as osp

def get_image_data_by_id(annot, img_id):
	for im_d in annot['images']:
		if img_id == im_d['id']:
			return im_d
	return None

annot_file = "singulation_test.json"
out_annot_file = "singulation_test_mini.json"
# annot_file = '/home/vincent/hd/datasets/MSCOCO/annotations/instances_val2014.json'
# out_annot_file = "val2014_mini.json"

with open(annot_file, 'r') as f:
	x = json.load(f)

out_x = {
	"info": x['info'],
	"images": [],
	"annotations": [],
	"categories": x['categories'],
	"licenses": x['licenses']
}

start_idx = 0
end_idx = 50

total_annots = len(x['annotations'])
end_idx = min(end_idx, total_annots-1)

img_id_data_cache = {}

for ix in xrange(start_idx, end_idx):
	anno = x['annotations'][ix]
	img_id = anno['image_id']
	if img_id not in img_id_data_cache:
		im_data = get_image_data_by_id(x, img_id)
		img_id_data_cache[img_id] = im_data 
	im_data = img_id_data_cache[img_id]
	if im_data is None:
		print("Could not find %d img id!"%(img_id))
		continue
	out_x['annotations'].append(anno)

for img_id, im_data in img_id_data_cache.items():
	out_x['images'].append(im_data)


with open(out_annot_file, "w") as f:
	json.dump(out_x, f)
	print("Saved to %s"%(out_annot_file))
