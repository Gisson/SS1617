#!/usr/bin/env python3
import sys

import ast
import traceback

from phply import phplex
from phply.phpparse import make_parser
from phply.phpast import *

from main import *

from collections import namedtuple
import re

DIVIDER=","
DEFAULT_CONFIG="../example_configs/example_config.cfg"

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
		logging.error("File "+fileName+" not found. Please retry")

	return rules












if __name__ == "__main__":
	enableDebug()

	parser = make_parser()

	lexer = phplex.lexer

	phpFile = sys.argv[1]
	with open(phpFile, "r") as f:
		code = f.read()

	if code:
		# FIXME: assuming it's php. Handle php inside HTML
		parser.parse('<?', lexer=lexer)
		try:
			try:
				lexer.lineno = 1
				rootNode = parser.parse(code, lexer=lexer)

				# FIXME: read config file and stuff
				if(len(sys.argv) > 2):
					config_file=sys.argv[2]
					logging.info("Using config file "+sys.arv[2])
				else:
					logging.info("No config file given, using default")
					config_file=DEFAULT_CONFIG
				config=readConfig(config_file)
				print(isTaintedNode(rootNode, config[0].name, config[0].entry_point, config[0].validation,config[0].sink))
			except SyntaxError as e:
			   print(e, 'near', repr(e.text))
		except:
			traceback.print_exc()


