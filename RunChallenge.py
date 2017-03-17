from AddressReader import *
from GeoIPLookup import *
from RDAPLookup import *
from CommandTerminal import *
from QueryFilter import *
import sys
import subprocess as sp
from blessings import Terminal
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
	time.sleep(1);
	queryFilter.printHeader();	
