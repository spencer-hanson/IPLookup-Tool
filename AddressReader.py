import re
import time

class AddressReader(object):
	def __init__(self, filename):
		self.filename = filename;
	def getAddresses(self):
		raw_data = self.__readFile();
		ip_data = [];
		regex = re.compile("(\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b)");
		for line in raw_data:
			matches = regex.findall(line);
			for match in matches:
				ip_data.append(match);		
		return ip_data;
	def __readFile(self):
		content = [];
		with open(self.filename) as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		return content;	
