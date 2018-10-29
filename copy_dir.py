import os
import os.path as osp
from shutil import copyfile
import glob
from natsort import natsorted as nts

if __name__ == '__main__':
    import argparse

    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t', dest='target_dir', help='target dir', 
                        required=True, type=str)
    parser.add_argument('-o', dest='output_dir', help='output dir',
                        required=True, type=str)
    # parser.add_argument('--publish', dest='publish', 
    #                     help='Publish segmentation results for each frame ',
    #                     action='store_true')
    parser.add_argument('--skip', dest='skip_frame', help='Frames to skip',
                            default=0, type=int)
    parser.add_argument('--ext', dest='ext', help='Only copy files with extension, if any',
                            default="", type=str)


    args = parser.parse_args()

    output_dir = args.output_dir
    if not osp.exists(output_dir):
        print("Created directory %s"%(output_dir))
        os.makedirs(output_dir)

    assert(osp.exists(args.target_dir))
    target_dir_files = nts(glob.glob(osp.join(args.target_dir, "*%s"%args.ext)))
    for ix,f in enumerate(target_dir_files):
        print("%d) %s"%(ix+1, f))
        if ix % args.skip_frame == 0:
            copyfile(f, osp.join(output_dir, f.split("/")[-1]))
            print("Copied %s to %s"%(f, output_dir))
