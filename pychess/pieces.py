import chess
import random

from pychess.logfacility import make_logger


class PieceExperiment:
    '''
    A chess board to place pieces which do not attack each other
    '''

    def __init__(self, loglevel, piece_type=chess.QUEEN,
                 piece_color=chess.WHITE, num_pieces=8, first_random=True):
        self.board = chess.Board().empty()
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.piece = chess.Piece(piece_type, piece_color)
        self.num_pieces = num_pieces
        self.first_random = first_random
        self.piece_positions = []
        self.logger = make_logger('PieceExperiment', loglevel)

    def place_random_piece(self):
        '''
        First piece in experiment may be set randomly
        '''
        random_square = random.choice(chess.SQUARES)
        self.board.set_piece_at(random_square, self.piece)
        self.piece_positions.append(random_square)

    def place_piece(self, startvalue):
        '''
        Find an unoccupied field which is not yet attacked
        and place a piece on it. Result may be the index of the
        field used or -1 if no field was found
        '''
        for square_index in range(startvalue, 64):
            attackers = self.board.attackers(self.piece_color, square_index)
            no_attacker = len(attackers) == 0
            free_square = not self.board.piece_at(square_index)
            if no_attacker and free_square:
                self.logger.debug(
                    'Found free field %s' % (
                        chess.square_name(square_index)
                    )
                )
                self.board.set_piece_at(square_index, self.piece)
                return square_index

        self.logger.debug('Unable to find free field!')
        return -1

    def run(self):
        '''
        Main method

        Uses backtracking to place pieces on board until the desired
        number of pieces has been placed
        '''

        if self.first_random and not len(self.piece_positions):
            self.place_random_piece()

        startvalue = 0
        iterations = 0

        while len(self.piece_positions) < self.num_pieces:
            iterations += 1
            place_result = self.place_piece(startvalue)
            if place_result != -1:
                self.piece_positions.append(place_result)
                startvalue = 0
            else:
                last = self.piece_positions.pop()
                self.board.remove_piece_at(last)
                startvalue = last + 1
                self.logger.debug(
                    'No free field found, backtracking from %s at index %s' % (
                        chess.square_name(last),
                        last
                    )
                )

            if iterations % 10000 == 0:
                self.logger.warning(
                    'Took %s iterations! Current number of pieces: %s\n%s' % (
                        iterations,
                        len(self.piece_positions),
                        self.board.unicode(),
                    )
                )

        self.logger.info('Placing finished!')
        self.logger.info('Placed %s pieces of %s on board' % (
            self.num_pieces, chess.piece_name(self.piece_type)
        ))
        self.logger.info('Took %s iterations' % iterations)
        print(self.board.unicode())
