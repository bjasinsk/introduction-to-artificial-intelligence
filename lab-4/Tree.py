class Tree:
    def __init__(self, type, attribute=None, value=None, dataset=None, children=None, class_value=None):
        self.type =type
        self.attribute = attribute
        self.value = value
        self.dataset = dataset
        self.class_value = class_value

        if children != None:
            self.children = children
        else:
            self.children = []

