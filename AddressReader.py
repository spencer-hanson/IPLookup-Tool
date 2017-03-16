import re

class AddressReader(object):
	def __init__(self, filename):
		self.filename = filename;
	def getAddresses(self):
		return self.__readFile();
	def __readFile(self):
		content = [];
		with open(self.filename) as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		return content;	
