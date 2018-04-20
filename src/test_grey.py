# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt #plt 用于显示图片
import matplotlib.image as mpimg #mpimg 用于读取图片
import numpy as np
import cv2

fn = './temppic/SH600115_20180327_20180404.png'
# lena = mpimg.imread(fn) #读取和代码处于同一目录下的lena.png
# # 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
# lena.shape #(512, 512, 3)
# plt.imshow(lena) # 显示图片
# plt.axis('off') # 不显示坐标轴
# plt.show()
# 
# # lena_1 = lena[:,:,0]
# # plt.imshow('lena_1')
# # plt.show()
# # 
# # plt.imshow('lena_1', cmap='Greys_r')
# # plt.show()
# 
# 
# def rgb2gray(rgb):
#     return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
# 
# gray = rgb2gray(lena)    
# # 也可以用 plt.imshow(gray, cmap = plt.get_cmap('gray'))
# plt.imshow(gray, cmap='Greys_r')
# plt.axis('off')
# plt.show()


img1=cv2.imread(fn,cv2.IMREAD_GRAYSCALE)
print(len(img1[0]))
print(img1[50])
print(img1[50][0])
print(type(img1))
print(type(img1[0]))
# for r in range(30,60):
#     img1[r]=0
m=32
img=cv2.resize(img1,(m,m),interpolation=cv2.INTER_CUBIC)
cv2.imshow('image',img)
for line in img:
    print(line)
cv2.waitKey(0) 