from HTMLParser import HTMLParser
import re

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
			print words
			self.listWords.extend(words)
	def getWords(self):
		return self.listWords
		
# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
file1 = open("sample","r")
text = file1.read()
parser.feed(text)
print parser.getWords()
