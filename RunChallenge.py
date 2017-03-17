from AddressReader import *
from GeoIPLookup import *
from RDAPLookup import *
from CommandTerminal import *
from QueryFilter import *
import sys
import subprocess as sp
from blessings import Terminal


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

	reader = AddressReader("list_of_ips.txt");
	addresses = reader.getAddresses();

	test_cases = ["4.2.2.2", "brokenaddress", addresses[0]];
	for test_case in test_cases:
		RDAPLookup.lookupRDAP(test_case);
		GeoIPLookup.lookupIP(test_case);


