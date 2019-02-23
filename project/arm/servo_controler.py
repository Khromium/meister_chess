#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Adafruit_PCA9685
import time
            
#サーボモーターをコントロールするためのクラス
class servo:
    #ChannelはPCA9685のサーボモーターを繋いだチャンネル
    #ZeroOffsetはサーボモーターの基準の位置を調節するためのパラメーターです
    
    def __init__(self, Channel, ZeroOffset):
        self.Channel = Channel
        self.ZeroOffset = ZeroOffset

        #Adafruit_PCA9685の初期化
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.pos = 90.0

    """角度を設定する関数です"""
    def set_pos(self, pos):
        #pulse = 150～650 : 0 ～ 180度
        #PCA9685はパルスで角度を制御しているため0~180のように角度を指定しても思った角度にはなりません
        #そこで角度の値からパルスの値へと変換します。PCA9685ではパルス150~650が角度の0~180に対応しているみたいです
        #下の式の(650-150)/180は1度あたりのパルスを表しています
        #それにpos(制御したい角度)を掛けた後、150を足すことでことで角度をパルスに直しています。
        #最後にZeroOffsetを足すことで基準にしたい位置に補正します
        pulse = (650.0-150.0)/180.0*pos + 150.0 + self.ZeroOffset
        self.pwm.set_pwm(self.Channel, 0, int(pulse))
        self.pos = pos
        time.sleep(0.004)
    
    def get_pos(self):
        return self.pos
    