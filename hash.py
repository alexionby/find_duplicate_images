import os,glob,shutil

import cv2
import numpy as np

from tqdm import tqdm

from PIL import Image

def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

images = glob.glob('redhead_final/*') 
print(len(images))
duplicates = dict()

for path in tqdm(images):
	image = cv2.imread(path)
	hash = dhash(image)
	samples = duplicates.setdefault(hash, [])
	samples.append(path)

for key in tqdm(duplicates):
	samples = duplicates[key]
	if len(samples) > 1:
		print(samples)

# print(duplicates)