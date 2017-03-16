from AddressReader import *
from GeoIPLookup import *
from RDAPLookup import *
import sys
import time
reader = AddressReader("list_of_ips.txt");
addresses = reader.getAddresses();


test_cases = ["4.2.2.2", "brokenaddress", addresses[0]];
for test_case in test_cases:
	RDAPLookup.lookupRDAP(test_case);
	GeoIPLookup.lookupIP(test_case);
