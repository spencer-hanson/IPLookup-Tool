from RDAPLookup import *
from GeoIPLookup import *
from AddressReader import *
from CommandTerminal import *
from QueryFilter import *
import re

class DataLoader(object):
	def __init__(self):
		self.data = {};
	def loadData(self, filename): #Load the inital file into data
		try:
			reader = AddressReader(filename);
			addresses = reader.getAddresses();
			for i in range(0, len(addresses)):
				self.data[addresses[i]] = "No Data";
		except (IOError):
			return "File {} not found or available".format(filename);
		return "Done!";

	def find(self, regex): #Find keys that match a regex
		results = [];
		try:
			regex = re.compile("({})".format(regex));
			for key, value in self.data.iteritems():
				if regex.match(key):
					results.append(key);
		except:
			print "Invalid regex!";
		finally:
			return results;
	def getSearchableData(self, key): #Get a dictionary of searchable values for a key
		search_data = {};
		if "GEO" in self.data[key]:
			tags = GeoIPLookup.getResultTags();
			for tag in tags:
				search_data[tag] = self.data[key]['GEO'][tag].strip('\n');
		if "RDAP" in self.data[key]:
			tags = RDAPLookup.getInterestingKeys();
			for tag in tags:
				search_data[tag] = self.data[key]['RDAP'][tag].strip('\n');
		return search_data;
	def findVal(self, regex, key): #Find a given regex in a key
		results = [];
		try:
			regex = re.compile("({})".format(regex));
			self.data[key]["SEARCH"] = self.getSearchableData(key);
			for tag, tag_data in self.data[key]["SEARCH"].iteritems():
				if regex.match(tag_data):
					results.append(tag_data);
		except:
			return ["Invalid regex!"];
		finally:
			return results;
	def getRawDataOf(self, key):
		return self.data[key];
	def getDataOf(self, key):#Get the given data of a key
		return str(self.data[key]);#TODO make data more readable
	def loadRDAP(self, key): #load data into a key
		if not self.hasData():
			print "No data to add to RDAP to!";
		else:
			if self.data[key] == "No Data":
				self.data[key] = {"RDAP": RDAPLookup.lookupRDAP(key)}; #Add data to this key
			else:
				if "RDAP" in self.data[key]:
					pass; #Data is already in this key for RDAP
				else:
					#Other data is in this key, must append
					self.data[key]["RDAP"] = RDAPLookup.lookupRDAP(key);
	def loadGeoIP(self, key): #load data into a key
		if not self.hasData(): #If there's no data
			print "No data to add a GeoLocation to!";	
		else:
			if self.data[key] == "No Data":
				self.data[key] = {"GEO": GeoIPLookup.lookupIP(key)};
			else:
				if "GEO" in self.data[key]:
					pass; #Data is already here
				else:
					#Other data is in key, must append
					self.data[key]["GEO"] = GeoIPLookup.lookupIP(key);

	def hasData(self): #Return if there is data loaded or not
		return self.data;
	
