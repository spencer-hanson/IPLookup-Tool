from RDAPLookup import *
from CommandTerminal import *
from QueryFilter import *


class DataLoader(object):
	def __init__(self, filename):
		self.filename = filename;
		self.data = {};
	def loadData(self):
		reader = AddressReader(self.filename);
		addresses = reader.getAddresses();
		for i in range(0, len(addresses)):
			self.data[addresses[i]] = "IP: {}".format(self.addresses[i]);
		return self.data;
	def loadGeoIP(self, key):
		if not self.data: #If there's no data
			return;
	def hasData(self): #Return if there is data loaded or not
		return self.data;
	
