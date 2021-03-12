import unittest
import chess

from gametree import GameTree
from boardrating import BoardRating


class TestGameTree(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()

    def test_backpropagation(self):
        tree = GameTree(self.board, depth=4, rating=BoardRating)
        tree.backpropagation()

    def no_test_fools_mate(self):
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
                print(node.board.unicode())

        self.assertTrue(count == 8, 'Something is broken haha')



if __name__ == '__main__':
    unittest.main()
