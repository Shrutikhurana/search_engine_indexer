def readDictionaryIndex():
	file = open("dictionary_index.txt")
	main_dictionary = {}
	for line in file:
		data =  line.split(":")
		key = data[0]
		values = []
		while (line.find('{') != -1):
			a = line.find('{')
			b = line.find('}')
			print a 
			print b
			print line [a+1:b]
			new_data = line[a+1:b]
			new_key = new_data.split(":")[0][1:-1]
			new_value = new_data.split(":")[1]
			print new_key
			print new_value
			new_dict = {}
			lenght= new_value.split(",")[0]
			m = new_value.find(',')
			new_value_iter = new_value[m+1:]
			print lenght
			length = lenght[2:]
			print length
			new_value_list =[]
			new_value_list.append(int(length))
			tag_list = []
			pos_list =[]
			while (new_value_iter.find('(') !=-1):
				c = new_value_iter.find('(')
				d = new_value_iter.find(')')
				new_value_iter_data =  new_value_iter[c+1:d]
				new_tuple = new_value_iter_data.split(',')
				tag_list.append(new_tuple[1][2:-1])
				pos_list.append(int (new_tuple[0][1:-1]))
				new_value_iter = new_value_iter[d+1:]
			new_value_list.append(tag_list)
			new_value_list.append(pos_list)
			new_dict[new_key] = new_value_list
			values.append(new_dict)
			line = line [b+1:]
		main_dictionary[key] = values
		return main_dictionary
main_dictionary = readDictionaryIndex()
print main_dictionary['10000']