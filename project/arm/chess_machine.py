import Adafruit_PCA9685
import arm.arm_controler as ac
from core.board import Board

class ChessMachine:
    def __init__(self, board, arm):
        self.board = board
        self.arm = arm

    def play_record(self, game):
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
                
        except KeyboardInterrupt  :  #Ctl+Cが押されたらループを終了
            print("\nCtl+C")
            self.arm.home_pos()

        except Exception as e:
            print(str(e))
    
    def human_control(self):
        try:
            while True:
                pos_str = input()
                if len(pos_str) == 2: # 普通の指令のとき
                    pos_str = pos_str.translate(str.maketrans({'a':'0','b':'1','c':'2','d':'3','e':'4','f':'5','g':'6','h':'7'}))
                    pos = int(pos_str[0]) + 8*(8 - int(pos_str[1]))
                elif pos_str == 'x':
                    pos = 64
                self.arm.move_pos(pos)
            self.arm.home_pos()
                
        except KeyboardInterrupt  :  #Ctl+Cが押されたらループを終了
            print("\nCtl+C")
            self.arm.home_pos()

        except Exception as e:
            print(str(e))