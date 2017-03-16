import json
import urllib2
import json
from pprint import pprint


class RDAPLookup(object):
	@staticmethod
	def lookupRDAP(ip_addr): #Perform a lookup of a given ips Registration Data
		query_url = "http://rdap.arin.net/bootstrap/ip/{}".format(ip_addr);
		data = {};
		try:
			response = urllib2.urlopen(query_url).read(); #Read response from server
			data = json.loads(response);
		except (urllib2.HTTPError, urllib2.URLError):
			print "[Debug] Error getting RDAP for {}".format(ip_addr);
			print "[Debug] {}".format(sys.exec_info()[0]);
			pass;
		finally:
			return data;
