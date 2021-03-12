import chess


class GameNode:
    '''
    One node in the chess game tree
    '''
    def __init__(self, board, parent, level):
        self.board = board
        self.children = []
        self.parent = parent
        self.level = level


class GameTree:
    '''
    A part of the huge chess game tree
    Do NOT call this with depth >= 5, unless u have a LOT of memory
    '''

    def __init__(self, board, depth, rating=None):
        self.rootNode = GameNode(board, None, 0)
        self.depth = depth
        self.rating = rating

        self.create_nodes(self.rootNode, self.depth)

    def create_nodes(self, node, depth):
        '''
        Recursively create children from given Node to a given depth
        '''
        if depth == 0:
            return
        level = self.depth - depth + 1
        for move in node.board.legal_moves:
            newboard = node.board.copy()
            newboard.push(move)
            new_node = GameNode(newboard, node, level)
            if self.rating is not None:
                rater = self.rating(new_node.board)
                new_node.rating = rater.rate()
            node.children.append(new_node)
            self.create_nodes(new_node, depth - 1)

    def traverse(self, node, node_filter=None):
        '''
        Recursive iterator exposing all node objects, to be called from extern
        to fetch node informations
        '''
        if node_filter is None or node_filter(node):
            yield node
        for child in node.children:
            yield from self.traverse(child, node_filter=node_filter)

    def backpropagation(self):
        for level in range(self.depth - 1, 0, -1):
            for node in self.traverse(
                self.rootNode,
                node_filter=lambda n: n.level == level
            ):
                ratings = [
                    child.rating
                    for child in node.children
                ]
                same = all(
                    ratings[0] == rating
                    for rating in ratings
                )
                if not same:
                    continue
                node.rating = ratings[0]


if __name__ == '__main__':

    board = chess.Board()
    tree = GameTree(board, depth=3)
    for node in tree.traverse(tree.rootNode):
        print(node.board.unicode())
