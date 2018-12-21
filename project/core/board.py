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
        :return: ゲーム結果
        """
        pgn = open(path)
        game_log = chess.pgn.read_game(pgn)
        if game_log is None:
            print("ゲームデータがありません")
            return
        self.board = game_log.board()
        if not self.board.is_valid():
            print("配置が不正です")
        return game_log

    def display_moves(self, game: chess.pgn.Game):
        """
        動きからゲームを再現します
        :param game: pgn.game データ
        :return:
        """
        for move in game.mainline_moves():
            self.check_move(move)
            self.board.push(move)
            self.check_state()
            print("---------------")
            print(self.board)
            print("---------------")
            print("\n")

    def check_state(self):
        """
        メモ。使わない
        :return:
        """
        if self.board.is_valid():  # ボードの状態が正常か
            # print("正常")
            pass
        if self.board.is_check():  # チェックか
            print("チェック!!")
        if self.board.is_checkmate():  # チェックメイトか
            print("チェックメイト!!")
        if self.board.is_game_over():  # ゲームオーバーか
            print("げーむおわりだお")
        if self.board.is_fivefold_repetition():  # 5回反復してるか
            print("it's fivefold repetition")

    def check_move(self, move: chess.Move):
        if not self.board.is_legal(move):
            print("動きが不正です")
        if self.board.is_castling(move) or self.board.is_kingside_castling(move):
            print("キャスリングだよ")
