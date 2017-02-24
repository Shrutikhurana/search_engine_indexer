def readfiles(path):

	list_file_names = []

	for (dirpath, dirnames, filenames) in walk(path):
		list_file_names.extend(filenames)
	
	for file_name in list_file_names:
		print file_name