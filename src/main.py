import logging, sys

from phply.phpast import *


def enableDebug():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("enabling debug...")


class Analyser:

    # list of tainted entry points
    # lstTaintedEntry[nodetype][nodeId][]
    lstTaintedEntry = {'Variable': {}}


    # list of tainted sinks
    lstTaintedSinks = []

    # list of sanitized sinks
    lstSanitizedSinks = []


    def __init__(self, vulnName, lstEntries, lstValidator, lstSinks):
        self.vulnName     = vulnName
        self.lstEntries   = lstEntries
        self.lstValidator = lstValidator
        self.lstSinks     = lstSinks

    # retuns true if the node has information coming from a tainted source
    def isTaintedNode(self, node):
        if isinstance(node, Node):
            return self.isNodeTainted(node)
        elif isinstance(node, list):
            t = False
            for item in node:
                if isinstance(item, Node):
                    t2 = self.isNodeTainted(item)
                    t = t or t2
            return t



    # this is basically a badly implemented Visitor pattern because the Node
    # class just accepts visitor functions, not objects...
    def isNodeTainted(self, node):
        if isinstance(node, (str, int, float)):
            return False

        if isinstance(node, InlineHTML):
            return False

        if isinstance(node, Constant):
            return False

        if isinstance(node, Variable):
            name = str(node.name)
            logging.debug('testing Variable: ' + name)
            try:
                tainted = self.isTainted(node)
            except KeyError:
                tainted = (name in self.lstEntries)
                self.setTainted(node, tainted)
            logging.debug('testing Variable: ' + name + ': ' + str(tainted))
            return tainted

        if isinstance(node, Assignment):
            logging.debug('testing Assignment')
            t = self.isTaintedNode(node.expr)
            if t:
                # mark the left value as tainted
                self.setTainted(node.node, t)
            # TODO: add it to the list of tainted nodes?
            return t

        if isinstance(node, ArrayOffset):
            logging.debug('testing ArrayOffset')
            t1 = self.isTaintedNode(node.node)
            t2 = self.isTaintedNode(node.expr)
            # TODO: add it to the list of tainted nodes? etc
            return t1 or t2

        if isinstance(node, BinaryOp):
            logging.debug('testing BinaryOp')
            t1 = self.isTaintedNode(node.left)
            t2 = self.isTaintedNode(node.right)
            # TODO: add it to the list of tainted nodes? etc
            return t1 or t2

        if isinstance(node, FunctionCall):
            logging.debug('testing FunctionCall')
            if node.name in self.lstValidator:
                # TODO: mark it as not tainted
                return False
            elif node.name in self.lstSinks:
                taintedArgs = self.isTaintedNode(node.params)
                if taintedArgs:
                    print("FOUND TAINTED SINK ("+self.vulnName+") in line " + str(node.lineno))
                    # TODO FAZER CENAS
                    return True
                else:
                    return False
            else:
                taintedArgs = self.isTaintedNode(node.params)
                # TODO FAZER CENAS
                return taintedArgs

        if isinstance(node, Parameter):
            logging.debug('testing Parameter')
            return self.isTaintedNode(node.node)

        print("Not implemented: " + str(type(node)))
        return False

    def setTainted(self, node, tainted):
        if isinstance(node, Variable):
            name = str(node.name)
            self.lstTaintedEntry['Variable'][name] = tainted;
        else:
            print("Not implemented: setTainted " + str(type(node)))

    def isTainted(self, node):
        if isinstance(node, Variable):
            name = str(node.name)
            return self.lstTaintedEntry['Variable'][name]
        else:
            print("Not implemented: setTainted " + str(type(node)))





