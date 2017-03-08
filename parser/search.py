from Tkinter import *
from operator import itemgetter
import webbrowser

def readbookkeeping():
	file = open("bookkeeping.json", "r")
	bookkeeping = {}
	lines  = file.read().split(",")
	for line in lines:
		if line == "{" or line == "}":
			continue
		else:
			line = line.strip()
			data = line.split(":")
			data[0] = data[0][1:-1]
			data[0] = data[0].replace("/","-")
			if len (data) > 1:
				data[1] = data[1][2:-1]
				bookkeeping[data[0]] = data[1]
	return bookkeeping


def readTFIDF():
	tfidf = {}
	file = open("tf-idf.txt", "r")
	
	for line in file:
		new_list = []
		data = line.split('-')
		content = data[1][1:-2].split(",")
		for value in content:
			main_content = value.split(":")
			dict_key = str(main_content[0][0:].replace("{","").strip())
			dict_key = dict_key.replace("\\\\","-")
			dict_key = dict_key[1:-1]
			print dict_key
			dict_value = main_content[1][:-1].strip()
			dict_value = dict_value.replace("}","")
			print dict_value
			dict_map ={}
			dict_map[dict_key] = float(dict_value)
			new_list.append(dict_map)
		tfidf[data[0]] = new_list
		
	return tfidf

def getSearchResultsByTFIDF(query_list):
	document_score = {}
	for word in query_list:
		print word
		if word in tfidf_index:
			document_list = tfidf_index[word]
			print document_list
			for document in document_list:
				keys = document.iterkeys()
				for key in keys:
					print key
					if key in document_score:
						document_score[key] = document_score[key] + document[key]
					else:
						document_score[key] = document[key]
	print document_score
	return sorted(document_score.items(), key=itemgetter(1),reverse = True)	

def callback():
	for widget in result_frame.winfo_children():
		widget.destroy()
	print text1.get()
	query_list = []
	query = text1.get()
	query_list = query.split()
	var = StringVar()

	label = Label(result_frame, textvariable = var)
	label.pack(side= TOP)
	
	scrollbar = Scrollbar(result_frame)
	scrollbar.pack( side = RIGHT, fill=Y )

	mylist = Listbox(result_frame, yscrollcommand = scrollbar.set,height =10, width = 800 )

	
	result = getSearchResultsByTFIDF(query_list)
	print result
	
	var.set("Result count: " + str(len(result)))
	
	for i in range(0,len(result)):
		mylist.insert(END, bookkeeping[result[i][0]])
	mylist.pack( side = LEFT, fill = BOTH )
	scrollbar.config( command = mylist.yview )
	mylist.bind( "<Double-Button-1>" , internet)

def internet(event):
	print "here"
	widget = event.widget
	selection=widget.curselection()
	value = widget.get(selection[0])
	print "selection:", selection, ": '%s'" % value
	webbrowser.open_new(value)

bookkeeping = readbookkeeping()	
print len(bookkeeping)	
tfidf_index = readTFIDF()
print len(tfidf_index)
master = Tk()
master.title("ICS Search")
master.geometry("1500x900")
frame = Frame(master)
frame.pack(side = TOP)
input_frame = Frame(frame)
input_frame.pack(side = TOP)
result_frame = Frame(frame)
result_frame.pack(side = BOTTOM)

text1 = Entry(input_frame, width =100)
text1.pack(side=LEFT)
b = Button(input_frame, text="Search", command= callback)
b.pack(side = RIGHT)

mainloop()