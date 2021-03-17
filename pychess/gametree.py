import chess
import logging
import multiprocessing
import uuid

from pychess.logfacility import make_logger


def create_children(node, level, rating):
    children = {}

    node_board = chess.Board(fen=node.board_fen)
    for move in node_board.legal_moves:
        node_board.push(move)

        new_node = GameNode(
            board_fen=node_board.fen(),
            move_uci=move.uci(),
            color=node_board.turn,
            parent_id=node.id,
            level=level
        )

        if rating is not None:
            rater = rating(node_board)
            new_node.rating = rater.rate()
            del rater

        children[new_node.id] = new_node
        node_board.pop()

    del node_board
    return children, node.id


class GameNode(object):
    '''
    One node in the chess game tree
    '''

    __slots__ = 'board_fen', 'move_uci', 'color', 'parent_id', 'level', 'id', 'rating'

    def __init__(self, board_fen, move_uci, color, parent_id, level):
        self.board_fen = board_fen
        self.move_uci = move_uci
        self.color = color
        self.parent_id = parent_id
        self.level = level
        self.id = uuid.uuid4()
        self.rating = None


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
            self.rootNode.id: self.rootNode,
        }

        self.child_map = {
            self.rootNode.id: [],
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

            with multiprocessing.Pool(4) as pool:
                pool.starmap_async(
                    create_children,
                    work,
                    callback=self.result_callback,
                    chunksize=10
                )
                pool.close()
                pool.join()

            self.logger.info('Worker finished on level %s' % (index + 1))

    def result_callback(self, results):
        for children, node_id in results:
            self.node_map.update(children)
            self.child_map[node_id] = list(children.keys())

    def traverse(self, node, node_filter=None):
        '''
        Recursive iterator exposing all node objects, to be called from extern
        to fetch node informations
        '''
        if node_filter is None or node_filter(node):
            yield node
        for child_id in self.child_map.get(node.id, []):
            child_node = self.node_map[child_id]
            yield from self.traverse(child_node, node_filter=node_filter)

    def children(self, node):
        return list(
            self.traverse(node, node_filter=lambda n: n.parent_id == node.id)
        )

    def backpropagation(self):
        for level in range(self.depth - 1, 0, -1):
            for node in self.traverse(
                self.rootNode,
                node_filter=lambda n: n.level == level
            ):

                children = self.children(node)
                if not children:
                    continue

                color = node.color

                win_positions = [
                    child
                    for child in children
                    if child.rating['finished']
                    and child.rating[color] == 1
                ]

                if win_positions:
                    node.rating[color] = 0.99
                    continue

                ratings = [
                    child.rating
                    for child in children
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
