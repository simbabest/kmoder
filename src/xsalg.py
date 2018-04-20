# -*- coding:utf-8 -*-
import cv2

def aHash(img,m):
    #缩放为 m*m=16*16
    img=cv2.resize(img,(m,m),interpolation=cv2.INTER_CUBIC)
    #转换为灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #s为像素和初值为0，hash_str为hash值初值为''
    s=0
    hash_str=''
    #遍历累加求像素和
    for i in range(m):
        for j in range(m):
            s=s+gray[i,j]
    #求平均灰度
    avg=s/(m*m)
    #灰度大于平均值为1相反为0生成图片的hash值
    for i in range(m):
        for j in range(m):
            if  gray[i,j]>avg:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'            
    return hash_str

#差值感知算法
def dHash(img,m):
    #缩放16*16
    img=cv2.resize(img,(m+1,m),interpolation=cv2.INTER_CUBIC)
    #转换灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(m):
        for j in range(m):
            if   gray[i,j]>gray[i,j+1]:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'0'
    return hash_str


def tHash(img,m):
    #缩放16*16
    img=cv2.resize(img,(m+1,m),interpolation=cv2.INTER_CUBIC)
    #转换灰度图
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hash_str=''
    #每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(m):
        for j in range(m):
            if gray[i,j]<85:
                hash_str=hash_str+'0'
            elif gray[i,j]>=85 and gray[j,j]<170:
                hash_str=hash_str+'1'
            else:
                hash_str=hash_str+'2'
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

def cmpHashNew(hash1,hash2):
    n=0
    #hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    #遍历判断
    for i in range(len(hash1)):
        #不相等则n计数+1或+0.5,n最终为相似度
        if int(hash1[i]) - int(hash2[i]) in [1,-1]:
            n = n + 1
        elif int(hash1[i]) - int(hash2[i]) in [2,-2]:
            n = n + 0.5
        else:
            pass
    return n