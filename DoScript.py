import sys
from QueryFilter import *
from blessings import Terminal
def shutdown(): #Do nothing on shutdown
	pass;
if __name__ == "__main__":
	if len(sys.argv) != 2: #Make sure there's only the name and script file in args
		print "Invalid syntax!";
		print "{} <filename>".format(sys.argv[0]); #Print syntax
	else:
		queryFilter = QueryFilter(shutdown);
		CommandTerminal.noPrintPrefix();
		queryFilter.runCommand("script {}".format(sys.argv[1]));
else:
	print "Must be run in main thread!";

