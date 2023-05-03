class Tree:
    def __init__(self, nodeData=None, children=None):
        self.nodeData = nodeData
        if children:
            self.children = children
        else:
            self.children = []

    def addChild(self, node):
        self.children.append(node)