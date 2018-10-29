import numpy as np
import numpy as np
import cv2
import argparse
import glob
import os
import os.path as osp

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", required = True,
	help = "Path where the original images are stored")
ap.add_argument("-o", "--output_dir", required = True,
	help = "Output where the resized images are stored")
ap.add_argument("-s", "--side", required = True,
	help = "Long side of the resized image", type=int)
ap.add_argument("-ext", "--ext", default = ".jpg",
	help = "Extension type of resized image")
#ap.add_argument("-q", "--query", required = True,
#	help = "Path to the query image")

args = vars(ap.parse_args())


side = args['side']

output_dir = args['output_dir']
ext_ = args['ext']
ext_ = ext_ if '.' in ext_ else "."+ext_

if not osp.exists(output_dir):
	os.makedirs(output_dir)

for img_path in glob.glob(args["dir"] + "/*.jpg"):

	# pokemon = img_path[img_path.rfind("/") + 1:].replace(".jpg", "")
	img = cv2.imread(img_path)

	h,w,_ = img.shape
	aspect_ratio = float(h) / w
	new_w = int(side/aspect_ratio)
	new_h =  int(side*aspect_ratio)

	if h > w:
		resized_img = cv2.resize(img,(new_w, side) )
	else:
		resized_img = cv2.resize(img, (side, new_h) )

	# cv2.imshow("resized", resized_img)
	# cv2.waitKey(0)

	base_img_path = img_path.split("/")[-1]
	base_img_path = base_img_path[:base_img_path.rfind('.')]
	out_path = osp.join(output_dir, base_img_path + ext_)

	cv2.imwrite(out_path, resized_img)

	print("%s resized -> %s"%(img_path, out_path))
