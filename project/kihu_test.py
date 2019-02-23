#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arm.arm_controler as ac
import arm.servo_controler as sc
from core.board import Board
from arm.chess_machine import ChessMachine

if __name__ == '__main__':
    arm = ac.arm()
    board = Board()
    machine = ChessMachine(board, arm)

    #print('ファイル名を入力してください')
    #path = input()
    game = board.load_pgn("./test.pgn")
    machine.play_record(game)
    