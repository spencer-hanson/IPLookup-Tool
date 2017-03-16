from bs4 import BeautifulSoup
import urllib2
import sys
class GeoIPLookup(object): #Static Class wrapper to get GeoLocational IP Lookup data
	@staticmethod
	def getResultTags():
		result_tags = ["ip", "countrycode", "countryname", "regioncode", "regionname", "city", "zipcode", "timezone", "latitude", "longitude", "metrocode"];
		return result_tags;


	@staticmethod
	def getEmptyData():
		data  = {"ip":"No Data", "countrycode":"No Data", "countryname":"No Data", "regioncode":"No Data", "regionname":"No Data", "city":"No Data", "zipcode":"No Data", "timezone":"No Data", "latitude":"No Data", "longitude":"No Data", "metrocode":"No Data"};
		return data;
	
	@staticmethod
	def lookupIP(ip_addr): #Look up a given ip address
		query_url = "http://freegeoip.net/xml/{}".format(ip_addr);
		result_tags = GeoIPLookup.getResultTags(); #Tags that return from the request from freegeoip
		data = GeoIPLookup.getEmptyData(); #Dict to store data in
		try:
			response = urllib2.urlopen(query_url).read();
			xmlSoup = BeautifulSoup(response, "lxml"); #Process xml
			response = xmlSoup.find('response'); #find the response tag
			for i in range(0, len(result_tags)):
				result = response.find(result_tags[i]).string; #Find each response tag and save them as a string
				if result == None: #Sometimes the database doesn't have info on a tag
					data[result_tags[i]] = "No Data";
				else:
					data[result_tags[i]] = result;
		except (urllib2.HTTPError, urllib2.URLError): #Catch errors for 404, 403 etc
			print "[Debug] Url Error for {}".format(ip_addr);
			print "[Debug] {}".format(sys.exec_info()[0]);
			pass;
		finally:
			return data;

	
