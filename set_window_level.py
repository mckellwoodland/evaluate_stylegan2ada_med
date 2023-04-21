# Inputs
import argparse
import os
import nibabel as nib
import numpy as np
from tqdm import tqdm

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, help='Path to input NIfTI images', required=True)
parser.add_argument('--output_path', type=str, help='Path to output NIfTI images', required=True)
parser.add_argument('--ww', type=int, help='Window Width', default=350)
parser.add_argument('--wl', type=int, help='Window Level', default=50)
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
ww = args.ww
wl = args.wl

# Iterate through input images.
for filename in tqdm(os.listdir(input_path)):
    # Read in input image.
    read_path = os.path.join(input_path, filename)
    img = nib.load(read_path)
    img_data = img.get_fdata()
    
    # Window the image with the appropriate width and level.
    img_data = np.clip(img_data, wl - (ww/2.), wl + (ww/2.))
    
    # Write out new image.
    write_path = os.path.join(output_path, filename)
    img_new = nib.Nifti1Image(img_data, img.affine, img.header)
    nib.save(img_new, write_path)
