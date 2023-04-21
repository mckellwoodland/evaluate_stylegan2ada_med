# Evaluating the Performance of StyleGAN2-ADA on Medical Images

This repository contains the preprocessing code for the paper "Evaluating the Performance of StyleGAN2-ADA on Medical Images"<sup>1</sup>.
The code inputs liver computed tomography scans in NIfTI format and outputs PNG images.

Directions for running the code:
- Set up the correct environment with the requirements.txt file: ```pip install -r requirements.txt``` in a standard Python environment.
- Window the data: ```python set_window_level.py --input_path [FOLDER CONTAINING ORIGINAL SCANS] --output_path [DESIRED OUTPUT FOLDER] --ww [WINDOW WIDTH] --wl [WINDOW LEVEL]```. The images in the input folder should be in NIfTI format.
- Discard non-liver images: ```python focus_slices.py --images_path [FOLDER CONTAINING WINDOWED SCANS] --masks_path [FOLDER CONTAINING MASKS] --output_path [DESIRED OUTPUT FOLDER]```. The images and their corresponding masks must have the same filename. Masks should be binary and should be in NIfTI format.
- Convert to PNG: ```python nifti_to_png.py --input_path [FOLDER CONTAINING FOCUSED SCANS] --output_path [DESIRED OUTPUT FOLDER] --rotate [INTEGER: 90, 180, or 270] --flip["v" OR "h"]```. Sometimes NiBabel reads in the images funny. If your PNG images aren't oriented right, you can always use the rotate and flip functions to reorient them. I usually need to do a rotation of 270 and a horizontal flip.

1. Woodland, M. et al. (2022). Evaluating the Performance of StyleGAN2-ADA on Medical Images. In: Zhao, C., Svoboda, D., Wolterink, J.M., Escobar, M. (eds) Simulation and Synthesis in Medical Imaging. SASHIMI 2022. Lecture Notes in Computer Science, vol 13570. Springer, Cham. https://doi.org/10.1007/978-3-031-16980-9_14
