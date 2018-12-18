import chess
import chess.pgn


class Board:
    """
    ボード関連のデータを取り仕切るクラス
    """

    def __init__(self):
        """
        データの読み込み
        """
        self.board = chess.Board()

    def save_svg(self, path):
        """
        SVGデータを保存
        :return:
        """
        with open(path, "w") as f:
            f.write(chess.svg.board(board=self.board))

    def load_pgn(self, path):
        """
        PGNファイルを読み込んでセットする
        :param path: ファイルパス
        :return:
        """
        pgn = open(path)
        game_log = chess.pgn.read_game(pgn)
        if game_log is None:
            return

        self.board = game_log.board()
        print(self.board)
        return game_log

    def display_moves(self, game: chess.pgn.Game):
        for move in game.mainline_moves():
            self.board.push(move)
            print("---------------")
            print(self.board)
            print("---------------")
            print("\n")

    def check_state(self):
        """
        メモ。使わない
        :return:
        """
        self.board.is_valid()  # ボードの状態が正常か
        self.board.is_legal()  # 正しい動きか
        self.board.is_check()  # チェックか
        self.board.is_checkmate()  # チェックメイトか
        self.board.is_game_over()  # ゲームオーバーか
        self.board.is_castling()
        self.board.is_kingside_castling()
