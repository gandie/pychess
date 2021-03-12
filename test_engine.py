import unittest
import random
import chess

from gametree import GameTree
from boardrating import BoardRating
from lbchess import LBChess


class TestLBChess(unittest.TestCase):

    def notest_checkmate_in_one(self):
        '''
        https://chess.stackexchange.com/questions/29535/what-moves-solve-this-mate-in-2

        1. Qbf4
        '''
        checkmate_in_one = '7r/1p3Q1p/2q5/3bk3/1Q6/2Pp4/r5PP/2KR4'

        self.board = chess.Board(fen=checkmate_in_one)
        white_player = LBChess(self.board, chess.WHITE, depth=1)
        next_move = white_player.next_move()
        self.board.push(next_move)
        print(next_move)
        print(self.board.unicode())
        self.assertTrue(
            str(next_move) == 'b4f4',
            'Did not detect checkmate in one!'
        )

    def test_checkmate_in_two(self):
        '''
        https://chess.stackexchange.com/questions/29535/what-moves-solve-this-mate-in-2

        1. d4+! exd3 2. Qbf4
        '''
        checkmate_in_two = '7r/1p3Q1p/2q5/3bk3/1Q2p3/2P5/r2P2PP/2KR4'
        self.board = chess.Board(fen=checkmate_in_two)
        white_player = LBChess(self.board, chess.WHITE, depth=3)
        next_move = white_player.next_move()
        self.board.push(next_move)
        print(next_move)
        print(self.board.unicode())
        self.assertTrue(
            str(next_move) == 'd2d4',
            'Did not detect first move of checkmate in two!'
        )
        some_move = random.choice(list(self.board.legal_moves))
        self.board.push(some_move)
        white_player.other_move(some_move)
        next_move = white_player.next_move()
        self.board.push(next_move)
        print(next_move)
        print(self.board.unicode())
        self.assertTrue(
            str(next_move) == 'b4f4',
            'Did not detect second move of checkmate in two!'
        )

    def notest_checkmate_in_three(self):
        '''
        https://chess.stackexchange.com/questions/34246/black-to-move-and-mate-in-3

        1. Ne2+ Kh1 2. Ng3+ hxg3 3. Bg4++
        '''
        checkmate_in_three = '5r1r/ppk3p1/8/2bB4/3n4/7b/PP4PP/RN1QR1K1'
        self.board = chess.Board(fen=checkmate_in_three)
        self.board.turn = chess.BLACK
        white_player = LBChess(self.board, chess.BLACK, depth=5)
        next_move = white_player.next_move()
        self.board.push(next_move)
        print(next_move)
        print(self.board.unicode())
        '''
        self.assertTrue(
            str(next_move) == 'd2d4',
            'Did not detect first move of checkmate in two!'
        )
        '''

class TestGameTree(unittest.TestCase):

    def setUp(self):
        self.board = chess.Board()

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
