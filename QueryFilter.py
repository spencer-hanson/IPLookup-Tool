from DataLoader import *
from GeoIPLookup import *
from RDAPLookup import *
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import timeit

class QueryFilter(object):
	def __init__(self, shutdown):
		self.data = {};
		self.shutdown = shutdown;
		self.dataLoader = DataLoader();
		self.queries = []; #Store results of queries in
	def runCommand(self, cmd):
		params = cmd.split(' ');
		if cmd == "CTRL_C" or cmd == "exit": #Handle exiting
			self.shutdown();
		elif cmd.startswith("help"): #Display help
			self.commandHelp(params);
		elif cmd.startswith("load"): #Load 
			self.commandLoad(params);
		else:
			if not self.dataLoader.hasData(): #If no data has been loaded
				print "No Data to query!"
				return;	
			command = self.getCommands().get(params[0], "None");
			if command != "None":
				command(params);
			else:
				print "Command not found! Type help for more info.";
	def getCommands(self):
		commands = {"info": self.commandInfo, "load": self.commandLoad, "print": self.commandPrint, "rdap": self.commandRDAP, "geo": self.commandGeo, "data": self.commandData, "summary": self.commandSummary, "search": self.commandSearch, "script":self.commandScript};
		return commands;

	def __validParams(self, params, numparams): #Check if parameters are valid
#Make sure the params match, subtract 1 for command at beginning of params
		if len(params)-1 != numparams: 
			self.__printInvalid();
			return False;
		else:
			return True;
	def __printInvalid(self):
		print "Invalid Syntax! Type help for more info.";
	def printHeader(self):
		self.printN("Query Filter v0.1 by Spencer Hanson");
	
	def __validVar(self, var):
		query_index = -1;
		if not var.startswith("$"): #Make sure the command is valid
			self.__printInvalid();
		else:
			try:
				query_index = int(var[1:]);
				tmp = self.queries[query_index]; #Used to throw error is var is invalid
			except:
				query_index = -1;
				print "Invalid var \'{}\'".format(var);
				pass;
		return query_index;
	def commandScript(self, params):
		print "Meow!";	
	def commandSearch(self, params):
		if not self.__validParams(params, 2):
			return;
		query_index = self.__validVar(params[1]);
		regex = params[2];
		if query_index != -1:
			for element in self.queries[query_index]:
				results = self.dataLoader.findVal(regex, element); #Find a regex in a key
				print "Results for {}".format(element);
				for result in results:
					self.printN(result);	
	def commandData(self, params):
		if not self.__validParams(params, 1):
			return;
		query_index = self.__validVar(params[1]);
		if query_index != -1:
			for element in self.queries[query_index]:
				self.printN(self.dataLoader.getDataOf(element));
	def commandPrint(self, params): #Print the given shell var
		if not self.__validParams(params, 1):
			return;
		query_index = self.__validVar(params[1]);
		if query_index != -1:
			for element in self.queries[query_index]:#print the value of the var list
				self.printN(element);

	def commandLoad(self, params): #Load data into memory
		if not self.__validParams(params, 1):
			return;
		filename = params[1];
		print "Loading \'{}\'".format(filename);
		print self.dataLoader.loadData(filename);

	def commandSummary(self, params): #Get a summary of the given var's data
		if not self.__validParams(params, 1):
			return;
		query_index = self.__validVar(params[1]);
		if query_index != -1:
			for element in self.queries[query_index]: #For each matching key
				raw_data = self.dataLoader.getSearchableData(element);
				for key, value in raw_data.iteritems(): #Print each informational item
					try:
						self.printN("{} - {}".format(key, value));
					except:
						self.printN("{} - No Data".format(key));
				self.printN("---");
	def commandRDAP(self, params): #Adds Registration data to a given key
		if not self.__validParams(params, 1):
			return;
		query_index = self.__validVar(params[1]);
		if query_index != -1:
			print "Loading in Registration Data for {} entries".format(len(self.queries[query_index]));
			pool = ThreadPool(4);
			start_time = timeit.default_timer();
			pool.map(self.dataLoader.loadRDAP, self.queries[query_index]);
			time_taken = timeit.default_timer() - start_time;
#			for element in self.queries[query_index]:
#				self.dataLoader.loadRDAP(element)
			print "Finished Loading in {} s".format(time_taken);
	def commandGeo(self, params): #Adds geographic data into a given key
		if not self.__validParams(params, 1):
			return;
		query_index = self.__validVar(params[1]);
		if query_index != -1:
			print "Loading in GeoLocation Data for {} entries".format(len(self.queries[query_index]));
			pool = ThreadPool(4);
			start_time = timeit.default_timer();
			pool.map(self.dataLoader.loadGeoIP, self.queries[query_index]);
			time_taken = timeit.default_timer() - start_time;
#			for element in self.queries[query_index]:
#				self.dataLoader.loadGeoIP(element);
			print "Finished Loading in {} s".format(time_taken);
	def commandInfo(self, params): #Get info about a given ip address
		if not self.__validParams(params, 1):
			return;
		ip_regex = params[1];
		print "Finding results with regex \'{}\'".format(ip_regex);
		key_results = self.dataLoader.find(ip_regex);
		print "Found {} results, storing in ${}".format(len(key_results), len(self.queries));
		self.queries.append(key_results);

	def printN(self, text):
		print "\\^noprefix$\\{}".format(text);

	def commandHelp(self, params): #Displays help
		self.printHeader();	
		self.printN("Commands:");
		self.printN("info <ip regex>");
		self.printN("    Displays information about given ip addresses, filtered by regex");
		self.printN("load <filename>");
		self.printN("    Loads a given file into memory, containing ip addresses");
		self.printN("print $<var>");
		self.printN("    prints out the contents of a var");
		self.printN("rdap $<var>");
		self.printN("    gets registration data for the given var");
		self.printN("geo $<var>");
		self.printN("    gets geographic data for the given var");
		self.printN("data $<var>");
		self.printN("    prints the data of the given var");
		self.printN("search $<var> <regex>");
		self.printN("    searches the fields of data from a given var for a regex");
		self.printN("script <filename>");
		self.printN("    runs a script of the given filename");
		self.printN("help");
		self.printN("   Displays this help message");
		self.printN("exit");
		self.printN("   Exits the terminal");
