import chess

from gametree import GameTree
from boardrating import BoardRating


if __name__ == '__main__':

    board = chess.Board()
    tree = GameTree(board, depth=5)
    count = 0
    for node in tree.traverse(tree.rootNode):
        rater = BoardRating(node.board)
        rating = rater.rate()
        if rating['finished']:
            count += 1
            print('Interesting board found! %s' % count)
            print(rating)
            print(node.board.unicode())
