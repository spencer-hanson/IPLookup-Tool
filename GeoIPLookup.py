from bs4 import BeautifulSoup
import urllib2

class GeoIPLookup(object):
	@staticmethod
	def lookupIP(ip_addr):
		query_url = "http://freegeoip.net/xml/{}".format(ip_addr);
		result_tags = ["ip", "countrycode", "countryname", "regioncode", "regionname", "city", "zipcode", "timezone", "latitude", "longitude", "metrocode"];
		#query_url = "http://freegeoip.net/xml/4.2.2.2";
		response = urllib2.urlopen(query_url).read();
		xmlSoup = BeautifulSoup(response, "lxml");
		response = xmlSoup.find('response');
		data = {};
		for i in range(0, len(result_tags)):
			result = response.find(result_tags[i]).string;
			if result == None:
				data[result_tags[i]] = "No Data";
			else:
				data[result_tags[i]] = result;
		return data;

