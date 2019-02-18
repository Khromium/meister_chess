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
        動きからゲームをディスプレイ上で再現します
        :param game: pgn.game データ
        :return:
        """
        for move in game.mainline_moves():
            self.check_move(move)
            route = self.piece_move(move)
            print(str(route))
            self.board.push(move)
            self.check_state()
            print("---------------")
            print(self.board)
            print("---------------")
            print("\n")
    
    def human_vs_human(self):
        game = chess.pgn.Game()
        while True:
            # 盤の表示
            print("---------------")
            print(self.board)
            print("---------------")
            print("\n")
            
            # 入力受け取り
            move = chess.Move.from_uci(input())
            while not self.board.is_legal(move):
                print("動きが不正です.もう一度入力してください．")
                move = chess.Move.from_uci(input())
            route = self._piece_move(move)
            
            # アーム動かす
            print('アーム動かす')
            '''
            '''

    def piece_move(self, move):
        """
        手からコマの動きを推定して，手先の動きを決める
        現状プロモーションは無視しています
        :param move: 指した手
        :return arm_route: 手先の経路，0~64のいずれかを要素に持つ配列，‐1は盤外を意味する
        """
        board_pre = str(self.board)  # 動かす前の盤面
        board_pre = board_pre.split()
        self.board.push(move)
        board_next = str(self.board)  # 動かした後の盤面
        board_next = board_next.split()
        self.board.pop()

        change_list = []
        move_to_list = []
        move_from_list = []
        for i in range(64):
            if board_next[i] != board_pre[i]:
                # マスの状態が変わってるときの処理
                if board_pre[i] != '.' and board_next[i] != '.':
                    # コマが変わったとき
                    change_list.append(i)
                elif board_pre[i] == '.':
                    # コマをとらずにただ移動したときの移動先
                    move_to_list.append(i)
                elif board_next[i] == '.':
                    # 移動した駒がもともといたマス もしくはアンパッサンで取られたマス
                    move_from_list.append(i)

        if len(move_from_list) == 1:
            if len(change_list) == 1:
                # コマをとるときの動作
                return [change_list[0], 64, move_from_list[0], change_list[0]]
            else:
                # コマを動かすだけの操作
                return [move_from_list[0], move_to_list[0]]
        else:
            if len(move_to_list) == 2:
                # キャスリング（本来キングから動かすべきだが気にしないことにする）
                return [move_from_list[0], move_to_list[1], move_from_list[1], move_to_list[0]]
            else:
                # アンパッサン
                if (move_to_list[0] - move_from_list[0]) == 8:
                    # move_from_list[0]がアンパッサンされるポーン
                    return [move_from_list[1], move_to_list[0], move_from_list[0], 64]
                else:
                    return [move_from_list[0], move_to_list[0], move_from_list[1], 64]

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
