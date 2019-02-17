#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time

# arm
class arm:
    def __init__(self, servo0, servo1, servo2, servo3, servo4, servo5):
        # pos_list : 0~3のモータの角度をマスごとに保存したリスト（64は盤外，65はホームポジション）
        self.pos_list = [[101,104, 93, 30],[ 96,103, 93, 31],[ 89,101, 93, 35],[ 84,100, 93, 40],[ 76,100, 93, 40],[ 71,101, 93, 39],[ 64,103, 93, 37],[ 58,105, 90, 35],
                        [103,102, 93, 45],[ 98, 96, 93, 50],[ 89, 97, 93, 55],[ 85, 96, 95, 60],[ 76, 96, 93, 58],[ 70, 95, 93, 58],[ 63, 95, 93, 53],[ 56, 94, 90, 48],
                        [108, 90, 90, 60],[ 99, 88, 88, 62],[ 93, 90, 89, 70],[ 85, 90, 90, 75],[ 76, 90, 88, 70],[ 69, 90, 89, 70],[ 61, 88, 85, 68],[ 55, 90, 85, 60],
                        [111, 90, 90, 74],[104, 80, 79, 74],[ 93, 60, 35, 45],[ 86, 73, 65, 75],[ 77, 73, 61, 73],[ 68, 70, 63, 73],[ 58, 70, 65, 74],[ 50, 80, 80, 74],
                        [116, 85, 81, 83],[110, 76, 75, 88],[ 97, 39, 20, 50],[ 88, 39, 20, 51],[ 76, 39, 20, 52],[ 65, 39, 20, 52],[ 56, 39, 20, 47],[ 47, 39, 20, 44],
                        [123, 75, 69, 86],[114, 30, 25, 86],[100, 30, 25, 86],[ 88, 50, 52, 98],[ 76, 50, 52, 98],[ 65, 50, 48, 98],[ 56, 50, 48, 98],[ 47, 50, 54, 95],
                        [123, 70, 50, 86],[118, 40, 20, 78],[100, 50, 40, 80],[0,0,0,0],[ 73, 34, 10, 75],[0,0,0,0],[0,0,0,0],[0,0,0,0],
                        [123, 70, 50, 86],[0,0,0,0],[114, 25, 10, 86],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],
                        [160, 30, 12, 50],[ 80,  5, 35, 75]]
        self.servo0 = servo0
        self.servo1 = servo1
        self.servo2 = servo2
        self.servo3 = servo3
        self.servo4 = servo4
        self.servo5 = servo5
        
        self.servo4.set_pos(67)
        self.servo5.set_pos(70)
        self.servo0.set_pos(80)
        self.servo1.set_pos(5)
        self.servo2.set_pos(35)
        self.servo3.set_pos(100)
        
        self.hand_flag = 0 # state:0->open 1->close
    
    def home_pos(self):
        s0 = int(self.servo0.get_pos())
        s1 = int(self.servo1.get_pos())
        s2 = int(self.servo2.get_pos())
        s3 = int(self.servo3.get_pos())
        
        if s1>=40:
            for  i in [x/(2*abs(40-s1)) for x in range(1, 2*abs(40-s1)+1)]:
                self.servo1.set_pos(s1 + i*(40-s1))
                time.sleep(0.1)
            time.sleep(0.1)
        diff = max(abs(50-s3), abs(50-s2))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo3.set_pos(s3 + i*(50-s3))
            self.servo2.set_pos(s2 + i*(50-s2))
        time.sleep(0.1)
        for  i in [x/abs(80-s0) for x in range(1, abs(80-s0)+1)]:
            self.servo0.set_pos(s0 + i*(80-s0))
        time.sleep(0.1)
        for  i in [x/25 for x in range(1, 26)]:
            self.servo2.set_pos(50 + i*(35-50))
            self.servo3.set_pos(50 + i*(75-50))
        for  i in [x/100 for x in range(1, 101)]:
            self.servo1.set_pos(30 + i*(5 -30))
            time.sleep(0.1)
        time.sleep(0.1)
        
    def move_pos(self, n):
        print(n)
        pos_diff = [self.pos_list[n][i] - self.pos_list[65][i] for i in range(4)]
        
        for  i in [x/abs(pos_diff[3]) for x in range(1, abs(pos_diff[3])+1)]:
            self.servo3.set_pos(self.pos_list[65][3] + i*pos_diff[3])
        time.sleep(0.1)
        for  i in [x/abs(pos_diff[0]) for x in range(1, abs(pos_diff[0])+1)]:
            self.servo0.set_pos(self.pos_list[65][0] + i*pos_diff[0])
        time.sleep(0.1)
        diff = max(abs(pos_diff[1]), abs(pos_diff[2]))
        for  i in [x/diff for x in range(1, diff+1)]:
            self.servo1.set_pos(self.pos_list[65][1] + i*pos_diff[1])
            self.servo2.set_pos(self.pos_list[65][2] + i*pos_diff[2])
        time.sleep(1)
        
        if self.hand_flag == 1:
            self.release()
            self.hand_flag = 0
        else:
            self.hold()
            self.hand_flag = 1
            
        self.home_pos()
    
    def hold(self):
        self.servo5.set_pos(90)
        time.sleep(0.3)
        self.servo5.set_pos(125)
        time.sleep(1)
    
    def release(self):
        self.servo5.set_pos(90)
        time.sleep(0.3)
        self.servo5.set_pos(70)
        time.sleep(1)
    