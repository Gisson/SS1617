import logging, sys

from phply.phpast import *


def enableDebug():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("enabling debug...")


# list of tainted sinks
lstTaintedSinks = []

# list of sanitized sinks
lstSanitizedSinks = []


# lookup table for node's tainted status
# e.g. tainted['Variable']['$q']
tainted = []

# retuns true if the node has information coming from a tainted source
def isTaintedNode(node, lstEntries, lstValidator, lstSinks):
    if isinstance(node, Node):
        return isNodeTainted(node, lstEntries, lstValidator, lstSinks)
    elif isinstance(node, list):
        t = False
        for item in node:
            if isinstance(item, Node):
                t2 = isNodeTainted(item, lstEntries, lstValidator, lstSinks)
                t = t or t2
        return t




# this is basically a badly implemented Visitor pattern. However, the Node
# class just accepts visitor functions, not objects...
def isNodeTainted(node, lstEntries, lstValidator, lstSinks):
    if isinstance(node, (str, int, float)):
        return False

    if isinstance(node, InlineHTML):
        return False

    if isinstance(node, Constant):
        return False

    if isinstance(node, Variable):
        name = str(node.name)
        logging.debug('testing Variable: ' + name)
        # TODO: add it to the list of tainted nodes?
        return (name in lstEntries)

    if isinstance(node, Assignment):
        t = isTaintedNode(node.expr, lstEntries, lstValidator, lstSinks)
        # TODO: mark node.node as tainted
        # TODO: add it to the list of tainted nodes?
        return t

    if isinstance(node, ArrayOffset):
        t1 = isTaintedNode(node.node, lstEntries, lstValidator, lstSinks)
        t2 = isTaintedNode(node.expr, lstEntries, lstValidator, lstSinks)
        # TODO: add it to the list of tainted nodes? etc
        return t1 or t2

    if isinstance(node, BinaryOp):
        t1 = isTaintedNode(node.left, lstEntries, lstValidator, lstSinks)
        t2 = isTaintedNode(node.right, lstEntries, lstValidator, lstSinks)
        # TODO: add it to the list of tainted nodes? etc
        return t1 or t2

    if isinstance(node, FunctionCall):
        if node.name in lstValidator:
            # TODO: mark it as not tainted
            return False
        elif node.name in lstSinks:
            taintedArgs = isTaintedNode(node.params, lstEntries, lstValidator, lstSinks)
            if taintedArgs:
                print("FOUND TAINTED SINK")
                # TODO FAZER CENAS
                return True
            else:
                return False
        else:
            taintedArgs = isTaintedNode(node.params, lstEntries, lstValidator, lstSinks)
            # TODO FAZER CENAS
            return taintedArgs

    if isinstance(node, Parameter):
        return isTaintedNode(node.node, lstEntries, lstValidator, lstSinks)

    print("Not implemented: " + str(type(node)))
    return False




#if __name__ == "__main__":



