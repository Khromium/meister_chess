#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time
import arm.arm_controler as ac
import arm.servo_controler as sc

# arm
class arm:
    def __init__(self):
        # サーボモータの処理帰化
        servo0 = sc.servo(Channel=0, ZeroOffset=-5.0)
        servo1 = sc.servo(Channel=1, ZeroOffset=-5.0)
        servo2 = sc.servo(Channel=2, ZeroOffset=-5.0)
        servo3 = sc.servo(Channel=3, ZeroOffset=-5.0)
        servo4 = sc.servo(Channel=4, ZeroOffset=-5.0)

        # pos_list : 0~3のモータの角度をマスごとに保存したリスト（64は盤外，65はホームポジション）
        #                       a                 b                 c                 d                 e                 f                 g                 h
        self.pos_list = [[101,114, 93, 30],[ 96,113, 93, 31],[ 89,111, 93, 35],[ 82,110, 93, 40],[ 75,110, 93, 40],[ 69,111, 93, 39],[ 61,113, 93, 37],[ 58,115, 90, 35],
                        [103,112, 93, 45],[ 98,114,100, 52],[ 84,107, 93, 55],[ 83,106, 95, 58],[ 73,103, 93, 60],[ 70,105, 93, 58],[ 61,105, 93, 53],[ 56,104, 90, 48],
                        [107,104, 90, 57],[ 99, 98, 88, 62],[ 93,100, 89, 70],[ 85,100, 90, 75],[ 74,100, 88, 75],[ 65,100, 89, 70],[ 60, 98, 85, 68],[ 53,100, 85, 60],
                        [111,100, 90, 74],[104, 90, 79, 74],[ 90, 70, 35, 45],[ 84, 83, 65, 75],[ 73, 80, 61, 73],[ 68, 80, 63, 73],[ 56, 80, 65, 74],[ 47, 90, 80, 74],
                        [116, 90, 81, 83],[107, 83, 68, 83],[ 97, 48, 20, 52],[ 84, 48, 20, 51],[ 72, 47, 20, 55],[ 59, 48, 20, 52],[ 51, 50, 20, 47],[ 43, 52, 20, 42],
                        [123, 83, 69, 86],[114, 50, 20, 55],[100, 50, 20, 63],[ 88, 50, 20, 70],[ 74, 50, 18, 70],[ 56, 50, 20, 70],[ 45, 50, 20, 62],[ 37, 50, 20, 52],
                        [130, 75, 50, 83],[121, 46, 20, 69],[110, 51, 20, 77],[ 94, 39, 10, 76],[ 72, 25,  5, 72],[ 52, 27,  3, 68],[ 38, 35, 11, 67],[ 31, 43, 20, 67],
                        [143, 70, 45, 86],[135, 70, 35, 90],[118, 25,  3, 75],[100, 25,  2, 85],[ 72, 25,  1, 86],[ 47, 25,  2, 84],[ 26, 25,  2, 75],[ 18, 25,  2, 55],
                        [160, 35,  8, 50],[ 80,  6, 35, 75]]
        self.servo0 = servo0
        self.servo1 = servo1
        self.servo2 = servo2
        self.servo3 = servo3
        self.servo4 = servo4
        
        self.servo4.set_pos(40)
        self.servo0.set_pos(80)
        self.servo1.set_pos(6)
        self.servo2.set_pos(35)
        self.servo3.set_pos(75)
        
        self.hand_flag = 0 # state:0->open 1->close
    
    def home_pos(self):
        s0 = self.servo0.get_pos()
        s1 = self.servo1.get_pos()
        s2 = self.servo2.get_pos()
        s3 = self.servo3.get_pos()
        
        if s1>=40:
            diff = int(0.6*abs(40-s1))
            for  i in [x/diff for x in range(1, diff+1)]:
                self.servo4.set_pos(self.servo4.get_pos())
                self.servo1.set_pos(s1 + i*(40-s1))
            s1 = 40
        diff = int(0.6 * max(abs(50-s3), abs(50-s2)))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo3.set_pos(s3 + i*(50-s3))
            self.servo2.set_pos(s2 + i*(50-s2))
        diff = int(0.6*abs(80-s0))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo0.set_pos(s0 + i*(80-s0))
        diff = int(0.6 * 25)
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo2.set_pos(50 + i*(35-50))
            self.servo3.set_pos(50 + i*(75-50))
        diff = int(0.6*abs(6-s1))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo4.set_pos(self.servo4.get_pos())
            self.servo1.set_pos(s1 + i*(6 - s1))
        
    def move_pos(self, n):
        print(n)
        s0 = self.servo0.get_pos()
        s1 = self.servo1.get_pos()
        s2 = self.servo2.get_pos()
        s3 = self.servo3.get_pos()
        pos_diff = [self.pos_list[n][0] - s0, self.pos_list[n][1] - s1, self.pos_list[n][2] - s2, self.pos_list[n][3] - s3]
        
        diff = int(0.6 * abs(pos_diff[3]))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo3.set_pos(self.pos_list[65][3] + i*pos_diff[3])
        diff = int(0.6 * abs(pos_diff[0]))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo0.set_pos(self.pos_list[65][0] + i*pos_diff[0])
        diff = int(0.6 * abs(pos_diff[1]))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo4.set_pos(self.servo4.get_pos())
            self.servo1.set_pos(self.pos_list[65][1] + i*pos_diff[1])
            self.servo2.set_pos(self.pos_list[65][2] + i*pos_diff[2])
        
        time.sleep(0.3)

        if self.hand_flag == 1:
            self.release()
            self.hand_flag = 0
        else:
            self.hold()
            self.hand_flag = 1
            
        self.home_pos()
    
    def hold(self):
        for  i in [x/46 for x in range(1, 47)]:
            self.servo4.set_pos(40 + i*(86-40))
        time.sleep(0.3)
    
    def release(self):
        for  i in [x/46 for x in range(1, 47)]:
            self.servo4.set_pos(86 + i*(40-86))
        time.sleep(0.3)
    