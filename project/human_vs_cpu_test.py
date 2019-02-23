#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arm.arm_controler as ac
import arm.servo_controler as sc
from core.board import Board
from arm.chess_machine import ChessMachine

if __name__ == '__main__':
    # servo * 6
    Servo0 = sc.servo(Channel=0, ZeroOffset=-5.0)
    Servo1 = sc.servo(Channel=1, ZeroOffset=-5.0)
    Servo2 = sc.servo(Channel=2, ZeroOffset=-5.0)
    Servo3 = sc.servo(Channel=3, ZeroOffset=-5.0)
    Servo4 = sc.servo(Channel=4, ZeroOffset=-5.0)
    
    arm = ac.arm(Servo0, Servo1, Servo2, Servo3, Servo4)
    board = Board()
    machine = ChessMachine(board, arm)

    machine.human_vs_cpu()