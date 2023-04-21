# Imports
import argparse
import os
import nibabel as nib
import numpy as np
from PIL import Image
from tqdm import tqdm

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--input_path', type=str, help='Path to input NIfTI images', required=True)
parser.add_argument('--output_path', type=str, help='Path to output NIfTI images', required=True)
parser.add_argument('--rotate', type=int, help='Options: 90, 180, or 270 degree rotations', default=None)
parser.add_argument('--flip', type=str, help='Options: "v" for vertical flip "h" for horizontal flip', default=None)
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
rotate = args.rotate
flip = args.flip

# Functions
def rescale_png(data):
  """
  Rescales the image to be in the range [0, 255] and have dtype int.
  Inputs:
    data (NumPy array): input image
  Outputs:
    (NumPy array): rescaled image
  """
  min_val = data.min()
  if min_val < 0:
    data += abs(min_val)
  else:
    data -= min_val
  data /= data.max()
  data = data * 255.
  data = data.astype(np.uint8)
  return data

def orient_png(data, rotate, flip):
  """
  Sometimes the images are read in from NiBabel funny. This function can bring
  the image back to the original orientation.
  Inputs:
    data (NumPy array): image data
    rotate: amount to rotate the image by (90, 180, or 270)
    flip: "v" for vertical flip, "h" for horizontal
  Outputs:
    (NumPy array)
  """
  # Rotate image.
  if rotate == 90:
    data = np.rot90(data)
  elif rotate == 180:
    data = np.rot90(np.rot90(data))
  elif rotate == 270:
    data = np.rot90(np.rot90(np.rot90(data)))
  # Flip image.
  if flip == "v":
    data = np.flip(data, axis=0)
  elif flip == "h":
    data = np.flip(data, axis=1)
  return data

# Main code.
for filename in tqdm(os.listdir(input_path)):
  img_prefix = filename.split(".")[0]
  img = nib.load(os.path.join(input_path, filename))
  img_data = img.get_fdata()

  num_slices = img_data.shape[2]
  for current_slice in range(num_slices):
    # Process data.
    data = img_data[:,:,current_slice]
    data = rescale_png(data)
    data = orient_png(data, rotate, flip)
    
    # Write out data.
    # The PNG images will have the same name as the original image with a "_i" added
    # to the end for the i-th slice.
    image_name = f"{img_prefix}_{current_slice}.png"
    write_path = os.path.join(output_path, image_name)
    img_pil = Image.fromarray(data)
    img_pil.save(write_path)
