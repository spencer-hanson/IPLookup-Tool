from AddressReader import *
from GeoIPLookup import *
reader = AddressReader("list_of_ips.txt");
addresses = reader.getAddresses();
GeoIPLookup.lookupIP(addresses[0]);

