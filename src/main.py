import logging, sys

from phply.phpast import *


def enableDebug():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("enabling debug...")


# list of tainted entry points
# lstTaintedEntry[nodetype][nodeId][]
lstTaintedEntry = {'Variable': {}}


# list of tainted sinks
lstTaintedSinks = []

# list of sanitized sinks
lstSanitizedSinks = []


# lookup table for node's tainted status
# e.g. tainted['Variable']['$q']
tainted = []

# retuns true if the node has information coming from a tainted source
def isTaintedNode(node, vulnName, lstEntries, lstValidator, lstSinks):
    if isinstance(node, Node):
        return isNodeTainted(node, vulnName, lstEntries, lstValidator, lstSinks)
    elif isinstance(node, list):
        t = False
        for item in node:
            if isinstance(item, Node):
                t2 = isNodeTainted(item, vulnName, lstEntries, lstValidator, lstSinks)
                t = t or t2
        return t



# this is basically a badly implemented Visitor pattern because the Node
# class just accepts visitor functions, not objects...
def isNodeTainted(node, vulnName, lstEntries, lstValidator, lstSinks):
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
            tainted = isTainted(node)
        except KeyError:
            tainted = (name in lstEntries)
            setTainted(node, tainted)
        logging.debug('testing Variable: ' + name + ': ' + str(tainted))
        return tainted

    if isinstance(node, Assignment):
        logging.debug('testing Assignment')
        t = isTaintedNode(node.expr, vulnName, lstEntries, lstValidator, lstSinks)
        if t:
            # mark the left value as tainted
            setTainted(node.node, t)
        # TODO: add it to the list of tainted nodes?
        return t

    if isinstance(node, ArrayOffset):
        logging.debug('testing ArrayOffset')
        t1 = isTaintedNode(node.node, vulnName, lstEntries, lstValidator, lstSinks)
        t2 = isTaintedNode(node.expr, vulnName, lstEntries, lstValidator, lstSinks)
        # TODO: add it to the list of tainted nodes? etc
        return t1 or t2

    if isinstance(node, BinaryOp):
        logging.debug('testing BinaryOp')
        t1 = isTaintedNode(node.left, vulnName, lstEntries, lstValidator, lstSinks)
        t2 = isTaintedNode(node.right, vulnName, lstEntries, lstValidator, lstSinks)
        # TODO: add it to the list of tainted nodes? etc
        return t1 or t2

    if isinstance(node, FunctionCall):
        logging.debug('testing FunctionCall')
        if node.name in lstValidator:
            # TODO: mark it as not tainted
            return False
        elif node.name in lstSinks:
            taintedArgs = isTaintedNode(node.params, vulnName, lstEntries, lstValidator, lstSinks)
            if taintedArgs:
                print("FOUND TAINTED SINK ("+vulnName+") in line " + str(node.lineno))
                # TODO FAZER CENAS
                return True
            else:
                return False
        else:
            taintedArgs = isTaintedNode(node.params, vulnName, lstEntries, lstValidator, lstSinks)
            # TODO FAZER CENAS
            return taintedArgs

    if isinstance(node, Parameter):
        logging.debug('testing Parameter')
        return isTaintedNode(node.node, vulnName, lstEntries, lstValidator, lstSinks)

    print("Not implemented: " + str(type(node)))
    return False

def setTainted(node, tainted):
    if isinstance(node, Variable):
        name = str(node.name)
        lstTaintedEntry['Variable'][name] = tainted;
    else:
        print("Not implemented: setTainted " + str(type(node)))

def isTainted(node):
    if isinstance(node, Variable):
        name = str(node.name)
        return lstTaintedEntry['Variable'][name]
    else:
        print("Not implemented: setTainted " + str(type(node)))


#if __name__ == "__main__":



