from phply.phpast import *


# The fields variable is shared by all instances of the sameclass. Therefore,
# it needs to be initialized in all classes, else Node.__repr__ will fail.
def initAttribute(node, field, fieldValue):
    if isinstance(node, list):
        for item in node:
            initAttribute(item, field, fieldValue)
    elif isinstance(node, Node):
        if not hasattr(node, field):
            setattr(node, field, fieldValue)
            if field not in node.fields:
                node.fields += [field,]

        for f in node.fields: # propagate to the children
            if hasattr(node, f):
                child = getattr(node, f)
                initAttribute(child, field, fieldValue)
    #else:
        #print(type(node))
