from AddressReader import *
from GeoIPLookup import *
from RDAPLookup import *
from CommandTerminal import *
from QueryFilter import *
import sys
import subprocess as sp
from blessings import Terminal
import objectpath
import time

commandTerminal = 0;
def shutdown():
	commandTerminal.printSystem("Stopping...");
	commandTerminal.end();

if __name__ == "__main__":
	sp.call('clear', shell=True);
	terminal = Terminal();
	terminal.clear();
	terminal.fullscreen();
	queryFilter = QueryFilter(shutdown);
	commandTerminal = CommandTerminal(terminal, queryFilter.runCommand);
	commandTerminal.start()
	queryFilter.printHeader();
	'''
	print "---";
	reader = AddressReader("ips.txt");
	addresses = reader.getAddresses();
	for address in addresses:
		print address;
	print "---";
	'''
	'''test_cases = ["4.2.2.2", "brokenaddress", addresses[0]];
	for test_case in test_cases:
		print RDAPLookup.lookupRDAP(test_case);
		print GeoIPLookup.lookupIP(test_case);
		time.sleep(5);
	'''
	#RDAP_data = RDAPLookup.lookupRDAP("4.2.2.2");

	#tree_obj = objectpath.Tree(RDAP_data);
	#print tuple(tree_obj.execute('$..label'))



