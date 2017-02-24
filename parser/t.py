import os
import glob
for filename in glob.iglob(os.path.join('Test','*')):
	with open(filename) as f:
		print filename
