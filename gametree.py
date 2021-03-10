import chess


class GameNode:
    '''
    One node in the chess game tree
    '''
    def __init__(self, board):
        self.board = board
        self.children = []


class GameTree:
    '''
    A part of the huge chess game tree
    Do NOT call this with depth >= 5, unless u have a LOT of memory
    '''

    def __init__(self, board, depth):
        self.rootNode = GameNode(board)
        self.createNodes(self.rootNode, depth)

    def createNodes(self, node, depth):
        '''
        Recursively create children from given Node to a given depth
        '''
        if depth == 0:
            return
        for move in node.board.legal_moves:
            newboard = node.board.copy()
            newboard.push(move)
            new_node = GameNode(newboard)
            node.children.append(new_node)
            self.createNodes(new_node, depth - 1)

    def traverse(self, node):
        '''
        Recursive iterator exposing all node objects, to be called from extern
        to fetch node informations
        '''
        yield node
        for child in node.children:
            yield from self.traverse(child)


if __name__ == '__main__':

    board = chess.Board()
    tree = GameTree(board, depth=3)
    for node in tree.traverse(tree.rootNode):
        print(node.board)
