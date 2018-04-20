# -*- coding: utf-8 -*-
"""HuangXin"""
import glob
import os
import sys
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog,
                             QMessageBox, QTableWidgetItem)
from PyQt5.QtGui import QIcon, QColor, QBrush
import cv2
import  numpy as np
from ui_xsd import Ui_XSD

# from openpyxl.styles import Color, Font, Alignment
# from openpyxl.styles.colors import BLUE, RED, GREEN, YELLOW
OUTPUT = '_output_'
USECOL = 'A,B,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,A,A,AB,AC,AD,AE,AF,AG,AH,AJ,AK'

def dHash(img):
    #缩放16*16
    img=cv2.resize(img,(17,16),interpolation=cv2.INTER_CUBIC)
    #转换灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(16):
        for j in range(16):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str

def cmpHash(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1，n最终为相似度
        if hash1[i]!=hash2[i]:
            n=n+1
    return n


class XSD(QDialog, Ui_XSD):
    """ XSD """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        # self.connect_signal()
        self.dirs = '##'
        # self.init_ui_params()
        

def main():
    app = QApplication(sys.argv)
    win = XSD()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
