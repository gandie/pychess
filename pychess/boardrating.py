import chess


class BoardRating:
    '''
    Pass a chess board and get rating
    '''

    def __init__(self, board):
        self.board = board

    def parse_result(self, rating):

        rating['finished'] = True

        result = self.board.result()
        white, black = result.split('-')

        if white == '1/2':
            white = 0.5
            black = 0.5
        else:
            white = int(white)
            black = int(black)

        rating[chess.WHITE] = white
        rating[chess.BLACK] = black
        return rating

    def rate(self):
        rating = {
            chess.WHITE: 0,
            chess.BLACK: 0,
            'finished': False,
        }

        # is the game already over?
        if self.board.is_game_over():
            return self.parse_result(rating)

        # XXX: do smart stuff here!
        return rating
