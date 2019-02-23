#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arm.arm_controler as ac
import arm.servo_controler as sc
from core.board import Board
from arm.chess_machine import ChessMachine
import threading
from time import sleep


class Dest:
    def __init__(self):
        self.st = "prichan"

class overall:

    def test(self):
        while True:
            self.dest.st = "hello"
            print(self.dest.st)
            sleep(1)

    def tests(self):
        while True:
            self.dest.st = "prichan"
            print(self.dest.st)
            sleep(1)

    def subete(self):
        self.dest = Dest()
        print(self.dest.st)
        th = threading.Thread(target=self.test)
        th.start()
        while True:
            self.dest.st = "prichan"
            print(self.dest.st)
            sleep(0.5)


if __name__ == '__main__':
   overall().subete()