# -*- coding:utf-8 -*-
import cv2
import  numpy as np
import glob
import pandas as pd

#均值哈希算法
def aHash(img):
    #缩放为8*8
    img=cv2.resize(img,(16,16),interpolation=cv2.INTER_CUBIC)
    #转换为灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #s为像素和初值为0，hash_str为hash值初值为''
    s=0
    hash_str=''
    #遍历累加求像素和
    for i in range(16):
        for j in range(16):
            s=s+gray[i,j]
    #求平均灰度
    avg=s/256
    #灰度大于平均值为1相反为0生成图片的hash值
    for i in range(16):
        for j in range(16):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'            
    return hash_str

#差值感知算法
def dHash(img):
    #缩放8*8
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

#Hash值对比
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

def xsd_test():
    fn1 = 'D:/Kmoder/images/SH600297/SH600297_20180108_20180118_2.0_-12.0_-7.0.png'
    fn2 = 'D:/Kmoder/images/SH600297/SH600297_20180109_20180119_4.0_-11.0_-6.0.png'
    img1=cv2.imread(fn1)
    img2=cv2.imread(fn2)
    hash1= aHash(img1)
    hash2= aHash(img2)
    print(hash1)
    print(hash2)
    n=cmpHash(hash1,hash2)
    print('均值哈希算法相似度：', n)
    
    
    hash1= dHash(img1)
    hash2= dHash(img2)
    print(hash1)
    print(hash2)
    n=cmpHash(hash1,hash2)
    print('差值哈希算法相似度：', n)
    
def xsd_matrix():
    datadir= 'D:/Kmoder/images/merge'
    pngfn = glob.glob(datadir + '/*.png')
    pngfn.sort()
    data = []
    for fn1 in pngfn[:100]:
        line = []
        for fn2 in pngfn[:100]:
            img1=cv2.imread(fn1)
            img2=cv2.imread(fn2)
            hash1= dHash(img1)
            hash2= dHash(img2)
            print(hash1)
            print(hash2)
            n=cmpHash(hash1,hash2)
            print('均值哈希算法相似度：',n)
            xsd = round(1-n / 256.0 ,2)
            line.append(xsd)
        data.append(line)
    df = pd.DataFrame(data)
    print(df)

if __name__ == '__main__':
    xsd_matrix()