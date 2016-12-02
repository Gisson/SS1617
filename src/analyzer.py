#!/usr/bin/env python
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
				print isTaintedNode(rootNode, ['$_POST',], ['mysql_escape_string',], ['mysql_query',])
			except SyntaxError as e:
			   print(e, 'near', repr(e.text))
		except:
			traceback.print_exc()


