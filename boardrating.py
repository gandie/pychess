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

        white_turn = self.board.turn == chess.WHITE

        # is there a winning move?
        winning_move = False
        for move in self.board.legal_moves:
            board_copy = self.board.copy()
            board_copy.push(move)
            if board_copy.is_checkmate():
                winning_move = True
                break

        if winning_move:
            if white_turn:
                rating[chess.WHITE] = 0.99
            else:
                rating[chess.BLACK] = 0.99
            return rating

        # XXX: do smart stuff here!
        return rating
