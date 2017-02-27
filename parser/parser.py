# -*- coding: utf-8 -*-
# encoding:utf-8

from HTMLParser import HTMLParser
import re
from stemming.porter2 import stem
import os
import glob
from os import walk
from nltk.corpus import stopwords 
import collections
import sys
reload(sys)
import site

sys.setdefaultencoding("UTF-8")

count_parser_words=0
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    
	tag =""
	list_of_words=[]	

	# list_of_words=[]	
	script = False
	def handle_starttag(self, tag, attrs):
		# print "Encountered a start tag:", tag
		
		self.tag = tag;
		if (tag == "script"):
			self.script = True
		
	def handle_endtag(self, tag):
		# print "Encountered an end tag :", tag	
			if self.script :
				self.script = False

	def handle_data(self, data):
		if self.script == False:
			words = re.sub(r'[^A-Za-z0-9]'," ",data).lower().split()
			for i in range(0,len(words)):
				word=words[i]
				self.list_of_words.append(word)
	
	def getWords(self):
		# print self.list_of_words
		global count_parser_words
		mywords = self.list_of_words
		self.list_of_words =[]
		count_parser_words=count_parser_words+len(mywords)
		# print count_parser_words," ","\n";
		return mywords
		
# instantiate the parser and fed it some HTML

class AllFilesParser():

	term_dictionary = {}

	def __init__(self): pass

	def create_term_dictionary(self,list_of_words):
		# print list_of_words
		self.term_dictionary={}
		for i in range(0,len(list_of_words)):
			word=list_of_words[i]
			# word not in stopwords.words('english')
			if (word) in self.term_dictionary: 
				self.term_dictionary[(word)].append(i)
				# self.term_dictionary[stem(word)]=sorted(self.term_dictionary[stem(word)])
			else:
				self.term_dictionary[(word)] = list()
				self.term_dictionary[(word)].append(i)
		# print self.term_dictionary
		# f1=open("term_dict.txt",'a')
		# for key,value in self.term_dictionary.iteritems():
		# 	f1.write(key+" "+str(value)+"\n")		
		return self.term_dictionary

	def parse_files(self, filename):
		try:
			parser = MyHTMLParser()
			parser.list_of_words=[]
			file1 = open(filename,"r")
			text = file1.read()
			parser.feed(text)
		except Exception as e:
			print e
		return self.create_term_dictionary(parser.getWords())
		

class parser_main:
	term_document=dict()
	count_documents=0

	def writefile(self):
		f=open("dictionary_index.txt","w")
		for key in sorted(self.term_document.iterkeys()):
   			# print "%s: %s" % (key, self.term_document[key])
			f.write(str(key)+": "+str(self.term_document[key])+'\n');
		f.close()	

	def readfiles(self,path):
		list_file_names = []
		for (dirpath, dirnames, filenames) in walk(path):
			filenames.sort(key=int)
			for file in filenames:
				list_file_names.append(path+"\\"+file)
				# print file
		for file_name in list_file_names:
			# print self.count_documents
			self.count_documents = self.count_documents + 1

			first_index = file_name.rfind("\\", 0,len(file_name) )
			name1 = file_name[first_index +1:]
			second_index = file_name.rfind("\\", 0,first_index  )
			name2 = file_name[second_index +1:]	
			new_file_name = name2	
			print new_file_name
			list_of_words=dict()
			list_of_words=AllFilesParser().parse_files(file_name);
			# word_counter=collections.Counter(list_of_words)
			# print type(list_of_words)
			for word in list_of_words:
				if word in self.term_document:
					document_freq_pos = {new_file_name:(len(list_of_words[word]),list_of_words[word])}
					self.term_document[word].append(document_freq_pos)
				else:
					self.term_document[word] = []
					document_freq_pos = {new_file_name:(len(list_of_words[word]),list_of_words[word])}
					self.term_document[word].append(document_freq_pos)
		# print self.term_document
			print len(self.term_document)	


# path=r'E:\search_engine_indexer\parser\Test';	
path=r'E:\search_engine_indexer\parser\webpages_raw\WEBPAGES_RAW';	

count_files=0

parser_ob=parser_main()
directory_names=[]
for (dirpath, dirnames, filenames) in walk(path):
	break
for directory in dirnames:
	directory_names.append(directory)
	# print directory
	directory_names.sort(key=int)
# print directory_names
for directory in directory_names:
	count_files=count_files+1
	parser_ob.readfiles(path+"\\"+directory);
	# print "folder count", count_files

parser_ob.writefile();			
print "The total number of document/files processed are",parser_ob.count_documents
print "The number of unique words are",len(parser_ob.term_document)
