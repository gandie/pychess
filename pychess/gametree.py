import chess


class GameNode:
    '''
    One node in the chess game tree
    '''
    def __init__(self, board_fen, move_uci, color, parent, level):
        self.board_fen = board_fen
        self.move_uci = move_uci
        self.color = color
        self.children = []
        self.parent = parent
        self.level = level


class GameTree:
    '''
    A part of the huge chess game tree
    Do NOT call this with depth >= 5, unless u have a LOT of memory
    '''

    def __init__(self, board, depth, rating=None):
        self.rootNode = GameNode(board.fen(), None, board.turn, None, 0)
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
        node_board = chess.Board(fen=node.board_fen)
        for move in node_board.legal_moves:
            node_board.push(move)

            new_node = GameNode(
                board_fen=node_board.fen(),
                move_uci=move.uci(),
                color=node_board.turn,
                parent=node,
                level=level
            )

            print('Node created on level %s' % level)
            if self.rating is not None:
                rater = self.rating(node_board)
                new_node.rating = rater.rate()
            node.children.append(new_node)
            node_board.pop()
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

                if not node.children:
                    continue

                color = node.color

                win_positions = [
                    child
                    for child in node.children
                    if child.rating['finished']
                    and child.rating[color] == 1
                ]

                if win_positions:
                    node.rating[color] = 0.99

                ratings = [
                    child.rating
                    for child in node.children
                ]
                if not ratings:
                    continue
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
