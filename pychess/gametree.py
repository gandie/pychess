import chess
import logging
import multiprocessing
import uuid

from pychess.logfacility import make_logger


def create_children(node, level, rating):
    children = []

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

        if rating is not None:
            rater = rating(node_board)
            new_node.rating = rater.rate()
        children.append(new_node)
        node_board.pop()

    return node, children


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
        self.id = uuid.uuid4()


class GameTree:
    '''
    A part of the huge chess game tree
    Do NOT call this with depth >= 5, unless u have a LOT of memory
    '''

    def __init__(self, board, depth, rating=None, loglevel=logging.DEBUG):
        self.rootNode = GameNode(board.fen(), None, board.turn, None, 0)
        self.depth = depth
        self.rating = rating

        self.node_map = {
            self.rootNode.id: self.rootNode
        }

        self.logger = make_logger('GameTree', loglevel)

        self.logger.info('Starting to build game tree ...')
        self.create_nodes(self.rootNode, self.depth)
        self.logger.info('GameTree built!')

    def create_nodes(self, node, depth):
        '''
        Build up tree
        '''

        for index in range(0, self.depth):
            work = []
            self.logger.info('Creating tree level %s' % (index + 1))
            for node in self.traverse(
                self.rootNode,
                node_filter=lambda n: n.level == index
            ):
                work.append((node, index + 1, self.rating))

            self.logger.info(
                'Starting worker on level %s, %s tasks' % (
                    index + 1, len(work)
                )
            )

            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                result = pool.starmap(create_children, work, chunksize=10)

            for parent, children in result:
                self.node_map[parent.id].children = children
                for child in children:
                    self.node_map[child.id] = child
            self.logger.info('Worker finished on level %s' % (index + 1))

    def result_callback(self, result):
        assert False
        parent, children = result
        self.node_map[parent.id].children = children
        for child in children:
            self.node_map[child.id] = child

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

                same = all(
                    ratings[0] == rating
                    for rating in ratings
                )
                if not same:
                    continue
                node.rating = ratings[0]


if __name__ == '__main__':

    board = chess.Board()
    tree = GameTree(board, depth=5)
    # for node in tree.traverse(tree.rootNode):
    #    print(chess.Board(fen=node.board_fen).unicode())
