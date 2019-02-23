#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time
import arm.arm_controler as ac
import arm.servo_controler as sc

"""制御を行うメインの部分です"""
if __name__ == '__main__':
    arm = ac.arm()

    try:
        while True:
            arm.move_pos(9)
            arm.move_pos(10)
            
            
    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
        arm.home_pos()

    except Exception as e:
        print(str(e))