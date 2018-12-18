from core.board import Board

if __name__ == '__main__':
    boad = Board()
    game = boad.load_pgn("./test.pgn")
    boad.display_moves(game)
