#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time
import arm_controler as ac
import servo_controler as sc

"""制御を行うメインの部分です"""
if __name__ == '__main__':
    # servo * 6
    Servo0 = sc.servo(Channel=0, ZeroOffset=-5.0)
    Servo1 = sc.servo(Channel=1, ZeroOffset=-5.0)
    Servo2 = sc.servo(Channel=2, ZeroOffset=-5.0)
    Servo3 = sc.servo(Channel=3, ZeroOffset=-5.0)
    Servo4 = sc.servo(Channel=4, ZeroOffset=-5.0)
    Servo5 = sc.servo(Channel=5, ZeroOffset=-5.0)
    
    arm = ac.arm(Servo0, Servo1, Servo2, Servo3, Servo4, Servo5)

    try:
        while True:
            arm.move_pos(9)
            arm.move_pos(10)
            
            
    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
        arm.home_pos()

    except Exception as e:
        print(str(e))