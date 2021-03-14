import chess
import random
import logging
import time


class RandomGame:
    '''
    A game of chess where both players move randomly
    '''

    def __init__(self, loglevel):
        self.board = chess.Board()
        self.logger = logging.getLogger('PieceExperiment')
        self.logger.setLevel(loglevel)

    def fullRandomStrategy(self):
        return random.choice(list(self.board.legal_moves))

    def run(self):
        while not self.board.is_game_over():
            next_move = self.fullRandomStrategy()
            self.board.push(next_move)
            print()
            print(self.board.unicode())
            time.sleep(.01)
        print(self.board.result())
        print(len(self.board.move_stack))
