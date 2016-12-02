import logging, sys

from phply.phpast import *


def enableDebug():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    logging.info("enabling debug...")


class Analyser:

    """ returns the line numbers of found sink functions that are tainted """
    def getTaintedSinkLines(self):
        if not self.hasRun:
            raise Exception("Analyser hasn't been run")
        return list(self.lstTaintedSinkLines)

    """ returns the line numbers of found sanitization functions """
    def getSanitizedSinkLines(self):
        if not self.hasRun:
            raise Exception("Analyser hasn't been run")
        return list(self.lstSanitizedSinkLines)

    def __init__(self, vulnName, lstEntries, lstValidator, lstSinks):
        logging.debug("initializing new analiser for " + vulnName + "...")
        self.vulnName     = vulnName
        self.lstEntries   = list(lstEntries)
        self.lstValidator = list(lstValidator)
        self.lstSinks     = list(lstSinks)


        # list of tainted entry points
        # lstTaintedEntry[nodetype][nodeId][]
        self.lstTaintedEntry = {'Variable': {}, 'Function': {}}
        # list of tainted sinks
        self.lstTaintedSinkLines = []
        # list of sanitized sinks
        self.lstSanitizedSinkLines = []
        self.hasRun = False

    # retuns true if the node has information coming from a tainted source
    def analyse(self, node):
        self.hasRun = True
        if isinstance(node, Node):
            return self.analyseNode(node)
        elif isinstance(node, list):
            t = False
            for item in node:
                if isinstance(item, Node):
                    t2 = self.analyseNode(item)
                    t = t or t2
            return t



    # this is basically a badly implemented Visitor pattern because the Node
    # class just accepts visitor functions, not objects...
    def analyseNode(self, node):
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
                logging.debug('already known: ' + name)
            except KeyError:
                logging.debug('not known: ' + name)
                tainted = (name in self.lstEntries)
                self.setTainted(node, tainted)
            logging.debug('testing Variable: ' + name + ': ' + str(tainted))
            return tainted

        if isinstance(node, Assignment):
            logging.debug('testing Assignment')

            t = self.analyse(node.expr)
            if t:
                # mark the left value as tainted
                self.setTainted(node.node, t)
            # TODO: add it to the list of tainted nodes?
            return t

        if isinstance(node, AssignOp): # aa .= bb
            logging.debug('testing AssignOp')

            t = self.analyse(node.right)
            if t:
                # mark the left value as tainted
                self.setTainted(node.left, t)
            # TODO: add it to the list of tainted nodes?
            return t

        if isinstance(node, ArrayOffset):
            logging.debug('testing ArrayOffset')
            t1 = self.analyse(node.node)
            t2 = self.analyse(node.expr)
            # TODO: add it to the list of tainted nodes? etc
            return t1 or t2

        if isinstance(node, BinaryOp):
            logging.debug('testing BinaryOp')
            t1 = self.analyse(node.left)
            t2 = self.analyse(node.right)
            # TODO: add it to the list of tainted nodes? etc
            return t1 or t2

        if isinstance(node, UnaryOp):
            logging.debug('testing UnaryOp')
            t1 = self.analyse(node.expr)
            # TODO: add it to the list of tainted nodes? etc
            return t1

        if isinstance(node, FunctionCall):
            fxName = node.name
            if isinstance(node.name, Variable): # function is a variable... $print_footer($single_lab);
                fxName = node.name.name
            logging.debug('testing FunctionCall ' + fxName )

            if fxName in self.lstValidator:
                logging.info("Found validation function for ("+self.vulnName+") in line " + str(node.lineno))
                self.lstSanitizedSinkLines += [node.lineno,]
                return False
            elif fxName in self.lstSinks:
                taintedArgs = self.analyse(node.params)
                if taintedArgs:
                    print("FOUND TAINTED SINK ("+self.vulnName+") in line " + str(node.lineno))
                    self.lstTaintedSinkLines += [node.lineno,]
                    # TODO FAZER CENAS
                    return True
                else:
                    return False
            else:
                # test if it's a function that has already been declared and is tainted
                try:
                    tainted = self.isTainted(node)
                except KeyError:
                    tainted = self.analyse(node.params)
                    self.setTainted(node, tainted)
                # TODO FAZER CENAS
                return tainted

        if isinstance(node, Node):
            if node.__class__.__name__ in ['Return', 'Parameter', 'Clone',
                                            'Break', 'Continue', 'Yield', 'Print',
                                            'Throw', 'Declare', 'Directive', 'Else', ]:
                logging.debug('testing ' + node.__class__.__name__)
                return self.analyse(node.node)
            elif node.__class__.__name__ in ['Block', 'Global', 'Static',
                                            'Finally', 'IsSet', 'Array', 'Default', ]:
                logging.debug('testing ' + node.__class__.__name__)
                t = False
                for item in node.nodes:
                    t2 = self.analyseNode(item)
                    t = t or t2
                return t
            elif node.__class__.__name__ in ['Echo', 'Print', ]:
                logging.debug('testing ' + node.__class__.__name__)
                name = node.__class__.__name__.lower()
                t = self.analyse(node.nodes)
                if name in self.lstSinks and t:
                    print("FOUND TAINTED SINK ("+self.vulnName+") in line " + str(node.lineno))
                    self.lstTaintedSinkLines += [node.lineno,]
                    # TODO FAZER CENAS
                return t
            elif node.__class__.__name__ in ['If', 'For', 'While', 'Foreach',
                                             'TernaryOp', 'PreIncDecOp', 'PostIncDecOp',
                                             'ForeachVariable', 'Cast', 'Exit',]:
                logging.debug('testing ' + node.__class__.__name__)
                t = False
                for field in node.fields:
                    t2 = self.analyse(getattr(node, field))
                    t = t or t2
                return t


        ## FIXME: need to check if declared functions are sinks. need a sink visitor

        if isinstance(node, Function): # function declaration
            logging.debug('testing Function')
            t = self.analyse(node.nodes)
            self.setTainted(node, t)
            return t

        if isinstance(node, Closure): # anonymous function
            logging.debug('testing Closure')
            # FIXME: should we do something with node.vars?
            t = self.analyse(node.nodes)
            #self.setTainted(node, t)
            return t

        if isinstance(node, ArrayElement): # function declaration
            logging.debug('testing ArrayElement')
            return self.analyse(node.value)


        print("Not implemented: analyseNode " + str(type(node))+" in line " + str(node.lineno))
        return False

    def setTainted(self, node, tainted):
        if isinstance(node, Variable):
            name = str(node.name)
            self.lstTaintedEntry['Variable'][name] = tainted;
        elif isinstance(node, Function) or isinstance(node, FunctionCall):
            name = str(node.name)
            self.lstTaintedEntry['Function'][name] = tainted;
        else:
            print("Not implemented: setTainted " + str(type(node))+" in line " + str(node.lineno))

    def isTainted(self, node):
        if isinstance(node, Variable):
            name = str(node.name)
            return self.lstTaintedEntry['Variable'][name]
        elif isinstance(node, Function) or isinstance(node, FunctionCall):
            name = str(node.name)
            return self.lstTaintedEntry['Function'][name]
        else:
            print("Not implemented: isTainted " + str(type(node))+" in line " + str(node.lineno))





