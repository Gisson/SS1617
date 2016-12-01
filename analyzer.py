import sys
from collections import namedtuple
import re

def divide_and_conquer(string,division):
	matchObj = re.match(r'((.*),(.*))*',string)
	
	for c in matchObj.group():
		print(c)


def readConfig(fileName):
	try:
		f = open(fileName, "r")
		rule = namedtuple("rule", "name entry_point validation sink")
		rules=[]
		ruletemp=[]
		text=f.readline()
		while(text != ""):
			if(text == "\n"):
				rules+=[rule( name=ruletemp[0], entry_point=ruletemp[1], validation=ruletemp[2], sink=ruletemp[3]),]
				ruletemp=[]
			ruletemp+=[text,]
			text=f.readline()
		rules+=[rule( name=ruletemp[0], entry_point=ruletemp[1], validation=ruletemp[2], sink=ruletemp[3]),]
		f.close()
	except IOError:
		print("File not found!!!!")

	return rules













if __name__ == "__main__":
	print(readConfig(sys.argv[1]))

