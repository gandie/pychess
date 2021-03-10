import chess
import random
import time

from gametree import GameTree
from boardrating import BoardRating


class LBChess:
    '''
    The most naive chess engine ever seen, written for absolutely
    no reason but boredom and for fun
    '''

    def __init__(self, board, color, fullrandom=False):
        self.board = board.copy()
        self.color = color
        self.fullrandom = fullrandom

    def next_move(self):
        '''
        Calculate next move and return it
        Testbed for experiments on how to play chess
        '''
        
        assert self.board.turn == self.color, 'Not my turn!'

        if self.fullrandom:
            move = random.choice(list(self.board.legal_moves))
            self.board.push(move)
            return move

        gametree = GameTree(self.board, depth=1)

        possible_nodes = []
        for node in gametree.traverse(gametree.rootNode):

            if node == gametree.rootNode:
                continue

            rater = BoardRating(node.board)
            rating = rater.rate()

            if rating[not self.color] == 0.99:
                print('Found dangerous position, skipping ...')
                continue
            if rating[self.color] == 1:
                print('Found winning move!')
                return node.board.pop()

            possible_nodes.append(node)

        if not possible_nodes:
            print(' No good move found! Will pick randomly')
            move = random.choice(list(self.board.legal_moves))
            self.board.push(move)
            return move

        # XXX: do smart things here! do smarter analysis / rating here
        move = random.choice(possible_nodes).board.pop()
        self.board.push(move)
        return move

    def other_move(self, move):
        assert self.board.turn != self.color, 'My turn!'
        self.board.push(move)

if __name__ == '__main__':

    games_played = 0
    limit = 100
    while games_played < limit:

        board = chess.Board()
        white_player = LBChess(board, chess.WHITE)
        black_player = LBChess(board, chess.BLACK, fullrandom=True)
        game_start = time.time()

        while True:
            w = white_player.next_move()
            black_player.other_move(w)
            board.push(w)
            #print()
            #print(board.unicode())

            if board.is_game_over():
                #print(board.unicode())
                print(board.result())
                games_played += 1
                break

            b = black_player.next_move()
            white_player.other_move(b)
            board.push(b)
            #print()
            #print(board.unicode())

            if board.is_game_over():
                #print(board.unicode())
                print(board.result())
                games_played += 1
                break

        print('Game took %s' % (time.time() - game_start))
