#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time
import arm.arm_controler as ac
import arm.servo_controler as sc

"""制御を行うメインの部分です"""
if __name__ == '__main__':
    # servo * 6
    Servo0 = sc.servo(Channel=0, ZeroOffset=-5.0)
    Servo1 = sc.servo(Channel=1, ZeroOffset=-5.0)
    Servo2 = sc.servo(Channel=2, ZeroOffset=-5.0)
    Servo3 = sc.servo(Channel=3, ZeroOffset=-5.0)
    Servo4 = sc.servo(Channel=4, ZeroOffset=-5.0)
    
    arm = ac.arm(Servo0, Servo1, Servo2, Servo3, Servo4)

    try:
        print('a1')
        arm.move_pos(56)
        print('a6')
        arm.move_pos(16)
        print('a6')
        arm.move_pos(16)
        print('out')
        arm.move_pos(64)
        print('b7')
        arm.move_pos(9)
        print('a6')
        arm.move_pos(16)
        print('b6')
        arm.move_pos(17)
        print('b7')
        arm.move_pos(9)
        
        time.sleep(1)
        
    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))