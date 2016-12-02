#!/usr/bin/env python3
import sys

import ast
import traceback

from phply import phplex
from phply.phpparse import make_parser
from phply.phpast import *

from libAnalyser import *

from collections import namedtuple
import re

DIVIDER=","
DEFAULT_CONFIG="../configs/default_config.cfg"

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
				if(len(ruletemp)>=4):
					rules+=[rule( name=ruletemp[0].strip(), entry_point=ruletemp[1].strip().split(DIVIDER), validation=ruletemp[2].strip().split(DIVIDER), sink=ruletemp[3].strip().split(DIVIDER)),]
				else:
					text=f.readline()
				ruletemp=[]
				text=f.readline()
			ruletemp+=[text,]
			text=f.readline()
		rules+=[rule( name=ruletemp[0].strip(), entry_point=ruletemp[1].strip().split(DIVIDER), validation=ruletemp[2].strip().split(DIVIDER), sink=ruletemp[3].strip().split(DIVIDER)),]
		f.close()
	except IOError:
		logging.error("File "+fileName+" not found. Please retry")
		sys.exit("Error reading file")

	return rules



def tryAnalyse(rule,rootNode):
	analyser = Analyser(rule.name, rule.entry_point, rule.validation, rule.sink)
	analyser.analyse(rootNode)
	taintedLines = analyser.getTaintedSinkLines()
	if len(taintedLines):
		for line in taintedLines:
			#TODO get the line content and print it
			print("Tainted sink for "+rule.name+" in line "+str(line)+":")
	else:
		sanitizationLines = analyser.getSanitizedSinkLines()
		for line in sanitizationLines:
			#TODO get the line content and print it
			print("Sanitized sink for "+rule.name+" in line "+str(line)+":")



def chooseConfigFile():
	# FIXME: read config file and stuff
	if(len(sys.argv) > 2):
		config_file=sys.argv[2]
		logging.info("Using config file "+sys.argv[2])
	else:
		logging.info("No config file given, using default")
		config_file=DEFAULT_CONFIG
	return readConfig(config_file)




if __name__ == "__main__":
	enableDebug()


	lexer = phplex.lexer

	phpFile = sys.argv[1]
	with open(phpFile, "r") as f:
		code = f.read()

	if code:
		# FIXME: assuming it's php. Handle php inside HTML
		parser = make_parser()
		if(not code.strip().startswith('<')):
			parser.parse('<?', lexer=lexer)
		lexer.lineno = 1
		config=chooseConfigFile()
		try:
			rootNode = parser.parse(code, lexer=lexer)
			for rule in config:
				tryAnalyse(rule,rootNode)
		except SyntaxError as e:
		   print(e, 'near', repr(e.text))

		except:
			traceback.print_exc()
