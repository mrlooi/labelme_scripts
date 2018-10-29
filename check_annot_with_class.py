import xml.etree.ElementTree as ET

import glob
import os.path as osp
import os 

def get_all_annots_with_class(annot_dirs, classname):
    if type(annot_dirs) != list:
        annot_dirs = [annot_dirs]

    annotdirs_with_class = {}
    for d in annot_dirs:
        annotdirs_with_class[d] = [] 
        annot_files = glob.glob(osp.join(d, '*.xml'))
        for f in annot_files:
            tree = ET.parse(f)
            element = tree.getroot()
            objs = [e for e in element.findall('object') if int(e.find("deleted").text) != 1 and e.find('name').text.lower().strip() == classname]

            # check if empty
            if len(objs) != 0:
                annotdirs_with_class[d].append(f)

    return annotdirs_with_class

if __name__ == '__main__':
# barcodes: barcodes,singulation
# envelopes: singulation

    import argparse
    
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-ad", "--annot_dir", required = True,
        help = "Annotation directory")
    ap.add_argument("-class", "--classname", required = True,
        help = "Classname")
    args = vars(ap.parse_args())

    annot_dir = args['annot_dir']

    annots_with_class = get_all_annots_with_class(annot_dir,args['classname'])
    # print(annots_with_class)
    print(len(annots_with_class[annot_dir]))

    # annot_dir = "./Annotations/singulation_test"
    # # annot_tar_dir = "./Annotations/singulation_barcode"
    # # img_dir = "./Images/singulation"
    # # img_tar_dir = "./Images/singulation_barcode"

    # annots_with_class = get_all_annots_with_class(annot_dir,'barcode')[annot_dir]
    # base_names = [f.split("/")[-1] for f in annots_with_class]
    # base_names = [f[:f.rfind('.')] for f in base_names]

    # for b in base_names:
    #     # print(osp.join(annot_dir,"%s.xml"%b),osp.join(annot_tar_dir,"%s.xml"%b))
    #     os.symlink(osp.join(annot_dir,"%s.xml"%b),osp.join(annot_tar_dir,"%s.xml"%b))
    #     os.symlink(osp.join(img_dir,"%s.jpg"%b),osp.join(img_tar_dir,"%s.jpg"%b))