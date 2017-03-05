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
import math

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
		# print self.term_dictionary
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
	cnt={} #count of the documents
	final_index_dic={}
	final_term_dic={} #word:term_frequency mapping
	final_document_dic={} #word:term_document frequency mapping
	tf_idf={} #tf-idf for term document pair

	def compute_tf_idf(self):
		# print self.final_term_dic;
		N=self.count_documents
		print len(self.final_term_dic),"****"
		# cnt=1
		# for word in self.final_term_dic:
		# 	print cnt,word
		# 	cnt=cnt+1

		for word in self.final_term_dic:
			# print word,self.final_term_dic[word]
			for i in range(0,len(self.final_term_dic[word])):
				for key,value in self.final_term_dic[word][i].iteritems():
					# print word,key,value
					if word not in self.tf_idf:
						self.tf_idf[word]=[]
						f=(float( math.log10(1+value)) * float(math.log10(float(self.count_documents)/ float(self.final_document_dic[word])) ) )
						print word,key,value,self.count_documents,f 
						# print f
						self.tf_idf[word].append({key:f})	
						# self.tf_idf[word].append({key: ( math.log10(1+value)* math.log10(self.count_documents/ self.final_document_dic[word] )) })
					else:
		
						f=(float( math.log10(1+value)) * float(math.log10(float(self.count_documents)/ float(self.final_document_dic[word])) ) )
						print word,key,value,self.final_document_dic[word],f 
						self.tf_idf[word].append({key:f})	

						# self.tf_idf[word].append({key: ( math.log10(1+value)* math.log10(self.count_documents/ self.final_document_dic[word] ) )	})

					
	def writefile(self):


		for word in self.term_document:
			self.final_document_dic[word]=self.cnt[word]

		# print self.final_document_dic

		a={}
		for word in self.term_document:
			self.final_index_dic[word]={self.cnt[word]:self.term_document[word]}

		parser_ob.compute_tf_idf()

		# WITH TERM FREQUENCY AND POSITIONS
		# f=open("dictionary_index.txt","w")
		# for key in sorted(self.term_document.iterkeys()):
  #  			# print "%s: %s" % (key, self.term_document[key])
		# 	f.write(str(key)+": "+str(self.term_document[key])+'\n');
		# f.close()	
			
		# # WITH DOCUMENT FREQUENCY,TERM FREQUECNY AND POSITIONS
		# f=open("dictionary_index1.txt","w")
		# for key in sorted(self.final_index_dic.iterkeys()):
  #  			# print "%s: %s" % (key, self.term_document[key])
		# 	f.write(str(key)+": "+str(self.final_index_dic[key])+'\n');
		# f.close()	

		# # WITH TERM, TERM FREQUENCY FOR EVERY DOCUMENT
		# f=open("dictionary_index2.txt","w")
		# for key in sorted(self.final_term_dic.iterkeys()):
  #  			# print "%s: %s" % (key, self.term_document[key])
		# 	f.write(str(key)+": "+str(self.final_term_dic[key])+'\n');
		# f.close()	

		print len(self.tf_idf)
		f=open("tf-idf.txt","w")
		for key in sorted(self.tf_idf.iterkeys()):
			f.write(str(key)+"-"+str(self.tf_idf[key])+"\n")			
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
				x=0
				if word in self.term_document:
					document_freq_pos = {new_file_name:(len(list_of_words[word]),list_of_words[word])}
					self.term_document[word].append(document_freq_pos)
					self.cnt[word]=len(self.term_document[word])	

					if word not in self.final_term_dic:
						x=x+len(list_of_words[word])
						self.final_term_dic[word]=[]
						self.final_term_dic[word].append({new_file_name:x})
					else:
						x=x+len(list_of_words[word])
						self.final_term_dic[word].append({new_file_name:x})

				else:
					self.term_document[word] = []
					document_freq_pos = {new_file_name:(len(list_of_words[word]),list_of_words[word])}
					self.term_document[word].append(document_freq_pos)
					self.cnt[word]=len(self.term_document[word])	

					if word not in self.final_term_dic:
						x=x+len(list_of_words[word])
						self.final_term_dic[word]=[]
						self.final_term_dic[word].append({new_file_name:x})
					else:
						x=x+len(list_of_words[word])
						self.final_term_dic[word].append({new_file_name:x})
				# print self.final_term_dic	

			# for word in self.cnt:
			# 	print word," ",self.cnt[word],"\n"		
			
		# print self.term_document
			# print len(self.cnt)
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

