import unittest
import chess

from pychess.boardrating import BoardRating
from pychess.gametree import GameTree


class TestGameTree(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()

    def test_fools_mate(self):
        tree = GameTree(self.board, depth=4, rating=BoardRating)
        count = 0

        for node in tree.traverse(
            tree.rootNode,
            node_filter=lambda n: n.level == 4
        ):
            if node.rating['finished']:
                count += 1
                print('Interesting board found! %s' % count)
                print(node.rating)
                board = chess.Board(fen=node.board_fen)
                print(board.unicode())

        self.assertTrue(count == 8, 'Unable to find all fools mate nodes!')


if __name__ == '__main__':
    unittest.main()
