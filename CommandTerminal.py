from blessings import Terminal
import time
import sys
import threading
import readchar
import subprocess as sp

class KeyVals(object): #Common keyvals
	# common
	LF = '\x0d'
	CR = '\x0a'
	ENTER = '\x0d'
	BACKSPACE = '\x7f'
	SUPR = ''
	SPACE = '\x20'
	ESC = '\x1b'

	# CTRL
	CTRL_A = '\x01'
	CTRL_B = '\x02'
	CTRL_C = '\x03'
	CTRL_D = '\x04'
	CTRL_E = '\x05'
	CTRL_F = '\x06'
	CTRL_Z = '\x1a'

	# ALT
	ALT_A = '\x1b\x61'

	# CTRL + ALT
	CTRL_ALT_A = '\x1b\x01'

	# cursors
	UP = '\x1b\x5b\x41'
	DOWN = '\x1b\x5b\x42'
	LEFT = '\x1b\x5b\x44'
	RIGHT = '\x1b\x5b\x43'
	
	CTRL_ALT_SUPR = '\x1b\x5b\x33\x5e'
	
	# other
	F1 = '\x1b\x4f\x50'
	F2 = '\x1b\x4f\x51'
	F3 = '\x1b\x4f\x52'
	F4 = '\x1b\x4f\x53'
	F5 = '\x1b\x4f\x31\x35\x7e'
	F6 = '\x1b\x4f\x31\x37\x7e'
	F7 = '\x1b\x4f\x31\x38\x7e'
	F8 = '\x1b\x4f\x31\x39\x7e'
	F9 = '\x1b\x4f\x32\x30\x7e'
	F10 = '\x1b\x4f\x32\x31\x7e'
	F11 = '\x1b\x4f\x32\x33\x7e'
	F12 = '\x1b\x4f\x32\x34\x7e'
	PAGE_UP = '\x1b\x5b\x35\x7e'
	PAGE_DOWN = '\x1b\x5b\x36\x7e'
	HOME = '\x1b\x5b\x48'
	END = '\x1b\x5b\x46'
	INSERT = '\x1b\x5b\x32\x7e'
	SUPR = '\x1b\x5b\x33\x7e'
	ESCAPE_SEQUENCES = (
	    ESC,
	    ESC + '\x5b',
	    ESC + '\x5b' + '\x31',
	    ESC + '\x5b' + '\x32',
	    ESC + '\x5b' + '\x33',
	    ESC + '\x5b' + '\x35',
	    ESC + '\x5b' + '\x36',
	    ESC + '\x5b' + '\x31' + '\x35',
	    ESC + '\x5b' + '\x31' + '\x36',
	    ESC + '\x5b' + '\x31' + '\x37',
	    ESC + '\x5b' + '\x31' + '\x38',
	    ESC + '\x5b' + '\x31' + '\x39',
	    ESC + '\x5b' + '\x32' + '\x30',
	    ESC + '\x5b' + '\x32' + '\x31',
	    ESC + '\x5b' + '\x32' + '\x32',
	    ESC + '\x5b' + '\x32' + '\x33',
	    ESC + '\x5b' + '\x32' + '\x34',
	    ESC + '\x4f',
	    ESC + ESC,
	    ESC + ESC + '\x5b',
	    ESC + ESC + '\x5b' + '\x32',
	    ESC + ESC + '\x5b' + '\x33',
	)

class PrintOutputter(object): #Hook into stdout/stderr
	def __init__(self, printer):
		self.printer = printer;
		self.origOut = sys.__stdout__;
		self.origErr = sys.__stderr__;
	def startManaging(self):
		sys.stdout = self;
		#sys.stderr = self; #Uncomment me!
		#self.origErr = sys.__stderr__;
		#self.origOut = sys.__stdout__;
	def stopManaging(self):
		self.origOut.flush();
		self.origErr.flush();
		sys.stderr = sys.__stderr__;
		sys.stdout = sys.__stdout__; 
	def write(self, txt):#Overwrite default write function
		proceed = False;
		if txt == '\n':
			return;
		[proceed, allTxt] = self.printer.doPrint(txt);
		if proceed:
			for newTxt in allTxt:
				self.origOut.write(newTxt);
        	self.origOut.flush();        
	def getOrigOut(self):
		return self.origOut;	

	def __getattr__(self, name):#Overwrite default attr of this class
		return self.origOut.__getattribute__(name);
class PrintManager(object):#Manages printer output
	def __init__(self, terminal, commandHook):
		self.x = 0;
		self.y = 1;
		self.currLine = 1;
		self.max_lines = 40;
		self.max_chars = 80;
		self.lines = [];
		self.command = "";
		self.caret = ">";
		self.terminal = terminal;
		self.commandHook = commandHook;
		print terminal.move(self.currLine, 1);
	def applyPrintOptions(self, options, prefix):#Apply a list of print options to a prefix
		for option in options.split(";"):
			if option == "noprefix":
				prefix = "";
			elif option.startswith("prefix"):#Can specify new prefix
				prefix = option.split(":")[1];
			elif option.startswith("name"):#Can specify name
				prefix = "(" + option.split(":")[1] + ") ";
		return prefix;				
	def doFormat(self, txt, x=0, y=-1): #Format a given piece of text given a line number
		prefix = "[System] ";#Default prefix is system
		if txt.startswith("\\^"):#If the options are set
			pos = txt.find("$\\");#Make sure it's formatted correctly
			if pos != -1:
				options = txt[2:pos];#Gather options
				txt = txt[pos+2:];
				prefix = self.applyPrintOptions(options, prefix);#Apply options	
		if y == -1:#If no line specified, add to next line
			y = self.currLine;
		prepend = "\x1b7\x1b[%d;%df" % (y, x);#Add location prefix needed by terminal
		newTxt = prefix + txt;
		diff = self.max_chars - len(newTxt) + 1; #Difference between typed text and max
		if diff > 0:
			newTxt = newTxt + " "*diff;#Space out difference to clear old lines
		else:
			newTxt = newTxt[:self.max_chars];#Only print up to max_chars
			#BUGBUG if text is larger it just cuts it off
		append = "%s\x1b8" % newTxt;#Add the append for the terminal
		msg = prepend+append;
		return msg;

	def doUserType(self, key): #Process user input
		if key == KeyVals.BACKSPACE:#Remove from input if backspace
			self.command = self.command[:-1]
		elif key == KeyVals.DOWN or key == KeyVals.UP or key == KeyVals.RIGHT or key == KeyVals.LEFT or key == KeyVals.PAGE_UP or key == KeyVals.PAGE_DOWN or key == KeyVals.HOME or key == KeyVals.END:
			pass; #Ignore annoying key inputs
		elif key == KeyVals.CTRL_C:#Send kill
			self.commandHook("CTRL_C");
		elif key == KeyVals.ENTER:#Run command
			self.commandHook(self.command);
			self.command = "";#Clear command buffer
		else:
			if not len(self.command)+len(self.caret) >= self.max_chars:
				self.command = self.command + key;

	def doPrint(self, txt): #Format print statement
		while len(self.lines) > self.max_lines: #Make sure we're within the bounds, remove excess lines
			tmp = self.lines.pop(0);
			self.currLine = self.currLine - 1;
		self.lines.append(txt);#Add current line
		self.currLine = self.currLine + 1;
		newTxt = [];
		line_count = 1; #Terminal line count starts at one for some reason
		for line in self.lines:#Re-append each line at the new line posisions
			newTxt.append(self.doFormat(line, y=line_count)); #Format line
			line_count = line_count+1;
		#Print caret
		newTxt.append(self.doFormat("\\^noprefix$\\" + self.caret+self.command, x=0, y=self.currLine));
		#Move Caret to new position
		newTxt.append(self.terminal.move(self.currLine-1, len(self.command)+1));
		return True, newTxt;

class CommandTerminal(threading.Thread): #Basic Command terminal
	def __init__(self, terminal, commandHook):
		threading.Thread.__init__(self);
		self.terminal = terminal;
		self.printmgr = PrintManager(self.terminal, commandHook); #Hook into stdout
		self.printer = PrintOutputter(self.printmgr); #Create new way to output
		self.stopped = False;
		self.listen = True;
	def run(self):
		self.printer.startManaging(); #Start managing output
		while not self.stopped:#Continue as long as not stopped
			if self.listen:
				self.printmgr.doUserType(readchar.readkey()); #Add the pressed key to the command
				#Put what the user has typed on the screen with the caret in front of it
				output = self.printmgr.doFormat("\\^noprefix$\\" + self.printmgr.caret+self.printmgr.command, x=0, y=self.printmgr.currLine)
				#Move the caret to the position of the text
				self.printer.getOrigOut().write(output+self.terminal.move(self.printmgr.currLine-1, len(self.printmgr.command)+1))
					
		self.printer.getOrigOut().flush(); #Flush stdout
		self.printer.stopManaging(); #Stop managing stdout
		print "\n[System] Terminated.";
	def setListening(self, listening):
		self.listen = listening;
	def getListening(self):
		return self.listen;
	def end(self):
		self.stopped = True;
	print_prefix = True;
	@staticmethod
	def noPrintPrefix():
		CommandTerminal.print_prefix = False;
	@staticmethod
	def removePrefix(text):
		if text.startswith("\\^"):
			endpos = text.find("$\\"); #Find end of prefix
			if endpos != -1:
				text = text[pos+2:]; #Remove it
		return text;
	@staticmethod
	def printThread(name, txt):
		if CommandTerminal.print_prefix:
			print "\\^name:{}$\\ {}".format(name, txt); #Print function for encoding output of a thread
		else:
			print txt;
	@staticmethod
	def printSystem(txt):
		if CommandTerminal.print_prefix:
			print "\\^prefix:[System]$\\ {}".format(txt); #Print function for encoding the output of system
		else:
			print txt;
	@staticmethod
	def printNoPrefix(txt):
		if CommandTerminal.print_prefix:
			print "\\^noprefix$\\ {}".format(txt);
		else:
			print txt;
