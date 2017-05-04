# IP Lookup Tool
Get geographical and domain registration data about given ip addresses
Python Challenge for Swimlane!


<img src="media/demo.gif" />

## Usage
The system is run through a commandline-like interface, with multiple commands for processing the data.

### Commands
<table>
	<tr><td><b>Command</b></td><td><b>Description</b></td><td><b>Example Usage</b></td></tr>
	<tr><td>find</td><td>Finds a given ip address given a regex, and stores it in a var</td><td>find 71\..</td></tr>
	<tr><td>load</td><td>Loads a file into memory, containing ip addresses</td><td>load list_of_ips.txt</td></tr>
	<tr><td>print</td><td>Prints info about a given query var</td><td>print $0</td></tr>
	<tr><td>rdap</td><td>Loads registration data for a given query var</td><td>rdap $0</td></tr>
	<tr><td>geo</td><td>Loads geographic data for a given query var</td><td>geo $0</td></tr>
	<tr><td>data</td><td>Prints the raw data of a given var</td><td>data $0</td></tr>
	<tr><td>search</td><td>Search a given query var's data for a given regex</td><td>search $0 US.</td></tr>
	<tr><td>script</td><td>Runs a script file, more info about this in the scripts section</td><td>script test.script</td></tr>
	<tr><td>save</td><td>Saves the data for a query var into a file, raw</td><td>save $0 data.txt</td></tr>
	<tr><td>help</td><td>Prints help message</td><td>help</td></tr>
	<tr><td>exit</td><td>Exits, same as CTRL + C</td></td><td>exit</td></tr>
</table>


## Scripts
Scripts can be made an automated easily, and can have any extension. Each line of the script is a command you would normally run in the terminal, and will exit on any error

Example Script:
~~~~
load ips.txt
find 77\..
geo $0
rdap $0
summary $0
search $0 KPN.
save $0 script_save.txt
exit
~~~~

Scripts can be run from within the terminal with the command
~~~~
script <filename>
~~~~
Or Via commandline with
~~~~
python DoScript.py <filename>
~~~~
## Installing/Running
To run this python challenge, you need a couple of dependencies, and must be running on a linux distribution. This is because certain python libraries used are not available on other platforms.
### Dependencies
* bs4
* lxml
* readchar
* blessings

You can install these dependencies with
~~~~
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev
sudo pip install bs4 lxml readchar blessings
~~~~

