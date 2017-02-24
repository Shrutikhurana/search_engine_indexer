from HTMLParser import HTMLParser
import re
from stemming.porter2 import stem
import os
import glob

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    
	tag =""
	listWords = []
	
	def handle_starttag(self, tag, attrs):
		print "Encountered a start tag:", tag
		self.tag = tag;
		
	def handle_endtag(self, tag):
		print "Encountered an end tag :", tag
		
		
	def handle_data(self, data):
		if self.tag not in ("script"):
			words = re.sub(r'[\W_]+'," ",data).lower().split()
			for word in words:
				print stem(word)
				self.listWords.append(stem(word))
	def getWords(self):
		return self.listWords
		
# instantiate the parser and fed it some HTML

class AllFilesParser():
	
	def parse_files(self, filename):
		parser = MyHTMLParser()
		file1 = open(filename,"r")
		text = file1.read()
		parser.feed(text)
		return parser.getWords()
		



AllFilesParser().parse_files();