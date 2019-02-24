import asyncio
import Adafruit_PCA9685
import arm.arm_controler as ac
import threading
from core.board import Board
import chess.engine
from assist.assistant import Assist


class ChessMachine:
    def __init__(self, board, arm, assist=False):
        self.board = board
        self.arm = arm
        if assist:
            # 参照をそのまま渡してマルチスレッド化することによって音声入力を並列でできるようにする。
            # TODO: 当日試してダメだったら無効にする
            threading.Thread(target=self._background).start()

    def _background(self):
        assist = Assist(self.board, self.arm)
        assist.activate()

    def play_record(self, game):
        """
        ゲームを順にたどってくれる関数。
        :param game: board.load_pgn でロードされたデータ
        :return:
        """
        try:
            for move in game.mainline_moves():
                self.board.check_move(move)
                route = self.board.piece_move(move)
                for pos in route:
                    self.arm.move_pos(pos)
                print(str(route))
                self.board.board.push(move)
                self.board.check_state()
            self.arm.home_pos()

        except KeyboardInterrupt:  # Ctl+Cが押されたらループを終了
            print("\nCtl+C")
            self.arm.home_pos()

        except Exception as e:
            print(str(e))

    def cpu_vs_cpu(self):
        async def main():
            transport, engine = await chess.engine.popen_uci("stockfish")

            while not self.board.check_game_over():
                cpu_result = await engine.play(self.board.board, chess.engine.Limit(time=0.100))
                route = self.board.piece_move(cpu_result.move)
                if len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                    for pos in route:
                        self.arm.move_pos(pos)
                    print(str(route))
                    self.board.board.push(cpu_result.move)
                    self.board.check_state()
                else:
                    print('正しく入力して下さい．終了するときはCtrl+C')
                    continue
                self.board.print_board()

            await engine.quit()

        asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
        asyncio.run(main())

    def cpu_vs_human(self):
        async def main():
            transport, engine = await chess.engine.popen_uci("stockfish")

            while not self.board.check_game_over():
                while True:
                    cpu_result = await engine.play(self.board.board, chess.engine.Limit(time=0.100))
                    route = self.board.piece_move(cpu_result.move)
                    if len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                        for pos in route:
                            self.arm.move_pos(pos)
                        print(str(route))
                        self.board.board.push(cpu_result.move)
                        self.board.check_state()
                        break
                    else:
                        print('正しく入力して下さい．終了するときはCtrl+C')
                        continue
                    self.board.print_board()

                while True:
                    move = input()
                    route = self.board.piece_move_str(move)
                    if self.board.turn:
                        break
                    elif len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                        for pos in route:
                            self.arm.move_pos(pos)
                        print(str(route))
                        self.board.board.push_san(move)
                        self.board.check_state()
                        break
                    else:
                        print('正しく入力して下さい．終了するときはCtrl+C')
                        continue

            await engine.quit()

        asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
        asyncio.run(main())

    def human_vs_cpu(self):
        async def main():
            transport, engine = await chess.engine.popen_uci("stockfish")

            while not self.board.check_game_over():
                while True:
                    move = input()
                    route = self.board.piece_move_str(move)
                    if self.board.turn:
                        break
                    elif len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                        for pos in route:
                            self.arm.move_pos(pos)
                        print(str(route))
                        self.board.board.push_san(move)
                        self.board.check_state()
                        break
                    else:
                        print('正しく入力して下さい．終了するときはCtrl+C')
                        continue

                while True:
                    cpu_result = await engine.play(self.board.board, chess.engine.Limit(time=0.100))
                    route = self.board.piece_move(cpu_result.move)
                    if len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                        for pos in route:
                            self.arm.move_pos(pos)
                        print(str(route))
                        self.board.board.push(cpu_result.move)
                        self.board.check_state()
                        break
                    else:
                        print('正しく入力して下さい．終了するときはCtrl+C')
                        continue
                    self.board.print_board()

            await engine.quit()

        asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
        asyncio.run(main())

    def human_vs_human(self):
        try:
            while True:
                move = input()
                route = self.board.piece_move_str(move)
                if len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
                    for pos in route:
                        self.arm.move_pos(pos)
                    print(str(route))
                    self.board.board.push_san(move)
                    self.board.check_state()
                else:
                    print('正しく入力して下さい．終了するときはCtrl+C')
                    continue
            self.arm.home_pos()

        except KeyboardInterrupt:  # Ctl+Cが押されたらループを終了
            print("\nCtl+C")
            self.arm.home_pos()

        except Exception as e:
            print(str(e))

    def human_control(self):
        try:
            while True:
                pos_str = input()
                if len(pos_str) == 2 and pos_str[0] in 'abcdefgh' and pos[1] in '12345678':  # 普通の指令のとき
                    pos_str = pos_str.translate(
                        str.maketrans({'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4', 'f': '5', 'g': '6', 'h': '7'}))
                    pos = int(pos_str[0]) + 8 * (8 - int(pos_str[1]))
                elif pos_str == 'x':
                    pos = 64
                else:
                    print('正しく入力して下さい．終了するときはCtrl+C')
                    continue
                self.arm.move_pos(pos)
            self.arm.home_pos()

        except KeyboardInterrupt:  # Ctl+Cが押されたらループを終了
            print("\nCtl+C")
            self.arm.home_pos()

        except Exception as e:
            print(str(e))
