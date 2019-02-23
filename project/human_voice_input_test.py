#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arm.arm_controler as ac
import arm.servo_controler as sc
import threading
from core.board import Board
from arm.chess_machine import ChessMachine
from assist.assistant import Assist

if __name__ == '__main__':
    arm = ac.arm()
    board = Board()
    machine = ChessMachine(board, arm, assist=True)
    machine.human_vs_human()
