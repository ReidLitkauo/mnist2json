# mnist2json.py
# A small Python3 script to convert image files from the MNIST database to JSON
# Uses the file format defined at: http://yann.lecun.com/exdb/mnist/
# Usage: mnist2json label_file.idx1-ubyte image_file.idx3-ubyte outfile.json
# Author: Reid Litkauo <https://reid.litkauo.com>
# License: Unlicense <http://unlicense.org>

import sys
import json
import binascii

# Call this function with opened file descriptors.
# The first two should be opened in 'rb' mode.
# The last one should be in 'w' mode.
def mnist2json(flabel, fimage, fout):
	
	# Make sure magic numbers are present
	if int.from_bytes(flabel.read(4), 'big') != 2049:
		print('Invalid .idx1 file')
		exit()
	if int.from_bytes(fimage.read(4), 'big') != 2051:
		print('Invalid .idx1 file')
		exit()
	
	# Grab number of labels/images to read
	count = int.from_bytes(flabel.read(4), 'big')
	if count != int.from_bytes(fimage.read(4), 'big'):
		print('Mismatching image count')
		exit()

	# Read rows & cols for each image
	rows = int.from_bytes(fimage.read(4), 'big')
	cols = int.from_bytes(fimage.read(4), 'big')

	# Initialization for images array (print this to fout)
	images = []

	# Read raw data
	for i in range(count):

		# Read one byte from the label file,
		# and associate with rows*cols bytes from the image file.
		# I slice the "image" string because for some reason...
		# hexlify returns a string that looks like: "b'01be ... ea'"
		# Yep, the string itself starts with b' (with the quote)
		# and ends with another quote.
		# So I slice those suckers out.
		images.append({
			'label': int.from_bytes(flabel.read(1), 'big'),
			'image': str(binascii.hexlify(fimage.read(rows*cols)))[2:-1],
		})

	# Write to desired output file
	fout.write( json.dumps(images) )



# Run as CLI
if __name__ == '__main__':

	# If we don't have the right number of arguments, print basic help and die
	if len(sys.argv) != 4:
		print('mnist2json label_file.idx1-ubyte image_file.idx3-ubyte outfile.json')
		exit()

	# Open files and call the function
	with open(sys.argv[1], "rb") as flabel:
		with open(sys.argv[2], "rb") as fimage:
			with open(sys.argv[3], "at") as fout:
				mnist2json(flabel, fimage, fout)
