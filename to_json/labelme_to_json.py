import numpy as np
import cv2
import json
import os.path as osp
import xml.etree.ElementTree as ET
import json

(CV2_MAJOR, CV2_MINOR, _) = cv2.__version__.split(".")
CV2_MAJOR = int(CV2_MAJOR)
CV2_MINOR = int(CV2_MINOR)

if __name__ == '__main__':
    annot_file = "../box/data_0_1506658963436.xml"  # xml file
    out_json_file = "../box/data_0_1506658963436.json"

    VIS = False
    if VIS:
        im_file = "../box/data_0_1506658963436.jpg"
        im = cv2.imread(im_file)
        im_copy = im.copy()

    et = ET.parse(annot_file)
    element = et.getroot()

    img_sz = element.find('imagesize')
    im_height = int(img_sz.find('nrows').text)
    im_width = int(img_sz.find('ncols').text)

    element_objects = element.findall('object')
    json_data = []
    for e in element_objects:
        if int(e.find('deleted').text) == 1:
            continue
        e_poly = e.find('polygon')
        e_cls = e.find('name').text
        e_pts = [( float(p.find('x').text), float(p.find('y').text) ) for p in e_poly.findall('pt')]
        e_pts = np.array(e_pts).astype(np.int32)
        print(e_pts)
        bbox = np.array([np.amin(e_pts, axis=0), np.amax(e_pts, axis=0)]).reshape(4)
        bbox[2:] -= bbox[:2]

        m = np.zeros((im_height, im_width), dtype=np.uint8)
        m = cv2.fillPoly(m, [e_pts], 255)
        cnt = cv2.findContours(m,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = cnt[0] if CV2_MAJOR != 3 else cnt[1]

        if len(cnt) == 0:
            continue

        cnt = cnt[0].squeeze()

        if VIS:
            cv2.drawContours(im_copy, [cnt], -1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("im_copy", im_copy)
            cv2.waitKey(0)

        json_data.append({'type': e_cls, 'score': 1.0, 'bbox': bbox.tolist(), 'contours': cnt.flatten().tolist()})

    with open(out_json_file, 'w') as f:
        json.dump(json_data, f)
    print("Saved to %s"%(out_json_file))
