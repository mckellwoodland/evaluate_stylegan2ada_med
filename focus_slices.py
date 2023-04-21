# Imports
import argparse
import os
import nibabel as nib
import numpy as np
from tqdm import tqdm

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--images_path', type=str, help='Path to input NIfTI images', required=True)
parser.add_argument('--masks_path', type=str, help='Path to input NIfTI masks', required=True)
parser.add_argument('--output_path', type=str, help='Path to output NIfTI images', required=True)
args = parser.parse_args()
images_path = args.images_path
masks_path = args.masks_path
output_path = args.output_path

for filename in tqdm(os.listdir(images_path)):
  # Code assumes that the images and their corresponding masks have the same filename.
  img = nib.load(os.path.join(images_path, filename))
  mask = nib.load(os.path.join(masks_path, filename))
  img_data = img.get_fdata()
  mask_data = mask.get_fdata()

  num_slices = img_data.shape[2]
  first_slice = 0
  last_slice = num_slices - 1
  first = False
  for current_slice in range(num_slices):
    if np.sum(mask_data[:, :, current_slice]) == 0.0 and first is False:
      first_slice += 1
    elif np.sum(mask_data[:, :, current_slice]) != 0.0:
      first = True
    elif np.sum(mask_data[:, :, current_slice]) == 0.0 and first is True:
      last_slice = current_slice
      if current_slice + 1 != num_slices:
        if np.sum(mask_data[:, :, current_slice+1]) == 0.0:
          break
  img_data = img_data[:, :, first_slice:last_slice]
  img = nib.Nifti1Image(img_data, img.affine, img.header)
  nib.save(img, os.path.join(output_path, filename))
