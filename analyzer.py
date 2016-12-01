import sys
from collections import namedtuple
import re

DIVIDER=","

def divide_and_conquer(string,division):
	divided = string.split(division) 
	return divided


def readConfig(fileName):
	try:
		f = open(fileName, "r")
		rule = namedtuple("rule", "name entry_point validation sink")
		rules=[]
		ruletemp=[]
		text=f.readline()
		while(text != ""):
			if(text == "\n"):
				rules+=[rule( name=ruletemp[0].strip(), entry_point=ruletemp[1].strip().split(DIVIDER), validation=ruletemp[2].strip().split(DIVIDER), sink=ruletemp[3].strip().split(DIVIDER)),]
				ruletemp=[]
				text=f.readline()
			ruletemp+=[text,]
			text=f.readline()
		rules+=[rule( name=ruletemp[0].strip(), entry_point=ruletemp[1].strip().split(DIVIDER), validation=ruletemp[2].strip().split(DIVIDER), sink=ruletemp[3].strip().split(DIVIDER)),]
		f.close()
	except IOError:
		print("File not found!!!!")

	return rules













if __name__ == "__main__":
	print(readConfig(sys.argv[1]))

