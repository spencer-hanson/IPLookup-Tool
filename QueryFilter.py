from DataLoader import *
class QueryFilter(object):
	def __init__(self, shutdown):
		self.data = {};
		self.shutdown = shutdown;
	def setData(self, data):
		self.data = data;
	def runCommand(self, cmd):
		params = cmd.split(' ');
		print params;
		print cmd;

		if cmd == "CTRL_C" or cmd == "exit":
			self.shutdown();
		elif cmd.startswith("help"):
			self.commandHelp(params);
		elif cmd.startswith("load"):
			self.commandLoad(params);
		else:
			if not self.data: #If data is empty
				print "No Data to query!"
				return;	
			command = self.getCommands().get(params[0], "None");
			if command != "None":
				command(params);
	def getCommands(self):
		commands = {"info": self.commandInfo, "load": self.commandLoad};
		return commands;
	def __validParams(self, params, numparams):
		if len(params)-1 != numparams: #Make sure the params match, subtract 1 for command at beginning of params
			print "Invalid Syntax!";
			return False;
		else:
			return True;
	def commandLoad(self, params):
		if not self.__validParams(params, 1):
			return;
		filename = params[1];
		
		print "Loading {}".format(filename);
	def commandInfo(self, params):
		if not self.__validParams(params, 1):
			return;
		ip = params[1];
		print self.data[ip];
	def commandHelp(self, params):
		print "MEOW!";
		
