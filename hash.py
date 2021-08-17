import os,glob,shutil

import cv2
import numpy as np

from tqdm import tqdm

from PIL import Image

# Difference Hash
def dHash(image, hash_size=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hash_size + 1, hash_size))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

# Average Hash
def get_aHash(image_dir):
 from functools import reduce
 image = Image.open(image_dir).resize((8, 8), Image.ANTIALIAS).convert('L')
 avg = reduce((lambda x,y:x+y),image.getdata())/64
 #aHash_value_binary = reduce(lambda x,y: str(x)+str(y),map(lambda i: 0 if i < avg else 1, image.getdata())) # Binary representation
 aHash_value_decimal = reduce(lambda x, y_z: x | (y_z[1] << y_z[0]),enumerate(map(lambda i: 0 if i < avg else 1, image.getdata())),0)
 return aHash_value_decimal


def get_pHash(image_dir):
	import cv2
	from functools import reduce
	image = cv2.imread(image_dir,cv2.IMREAD_GRAYSCALE)
	image = cv2.resize(image,(32,32),interpolation=cv2.INTER_AREA)
	image = image.astype('float')
	image = cv2.dct(image) 
	image = cv2.resize(image,(8,8))
	avg_dct = sum(sum(image))/64
	image = sum(image.tolist(),[])
	#pHash_value_binary = reduce(lambda x,y:str(x)+str(y),map(lambda x: 0 if x<avg_dct else 1 , image[::-1]))  #It doesn't matter the order of the combination, as long as the pictures compared are the same
	pHash_value_decimal = reduce(lambda x, y_z: x | (y_z[1] << y_z[0]),enumerate(map(lambda i: 0 if i < avg_dct else 1, image)),0)
	return pHash_value_decimal 


# dist between two hashes
def hamming(h1,h2):
	d = h1^h2
	res = bin(d).count('1')
	return res   
	 

images = glob.glob('trainA/*') 
print(len(images))
duplicates = dict()

for path in tqdm(images):
	image = cv2.imread(path)
	hash = dHash(image)
	samples = duplicates.setdefault(hash, [])
	samples.append(path)

for key in tqdm(duplicates):
	samples = duplicates[key]
	if len(samples) > 1:
		print(samples)

# print(duplicates)