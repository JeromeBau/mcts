class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


class SearchTree(Tree):
    def __init__(self):
        super(SearchTree, self).__init__()
        self.average_path_value = None
        self.passes = 0
        self.full_path = []
