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
            self._piece_move(move)
            self.board.push(move)
            self.check_state()
            print("---------------")
            print(self.board)
            print("---------------")
            print("\n")

    def _piece_move(self, move):
        """
        手からコマの動きを推定します
        :param move: 指した手
        :return:
        """
        board_pre = str(self.board) # 動かす前の盤面
        board_pre = board_pre.split()
        self.board.push(move)
        board_next = str(self.board) # 動かした後の盤面
        board_next = board_next.split()
        self.board.pop()

        for i in range(64):
            if(board_next[i] != board_pre[i]):
                # マスの状態が変わってるときの処理
                if(board_pre[i] != '.' and board_next[i] != '.'):
                    # コマが変わったとき
                    print("change " + str(i) + " : " + str(board_pre[i]) + " to " + str(board_next[i]) + "\n")
                elif(board_pre[i] == '.'):
                    # コマをとらずにただ移動したときの移動先
                    print(str(board_next[i]) + " move to " + str(i) + "\n")
                elif(board_next[i] == '.'):
                    # 移動した駒がもともといたマス もしくはアンパッサンで取られたマス
                    print(str(board_pre[i]) + " move from " + str(i) + "\n")
                    

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
