import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import json
import piexif
import piexif.helper
import hashlib
import pandas as pd
import numpy as np
my_img = Image.open('/home/pratyush/Downloads/Imaage/Experiment/Photo_self.jpeg')
# cv2_imshow(my_img)
plt.imshow(my_img)
pix = my_img.load()
size = my_img.size
mod = min(size)
key = hashlib.md5(key.encode()).hexdigest()
print(key)
key_length = len(key)
key_array = []
key_sum = sum(key_array)

for key in key:
    key_array.append(ord(key)%mod)
for k in range (2,key_length):
    for i in range (0,size[0],k):
        y1=i
        y2=(i+k*(key_array[k%(key_length)])**key_length)%size[0]
        for j in range(0,size[1]):
            x=j
            pixel1 = pix[y1,x]
            pixel2 = pix[y2,x]
            pix[y1,x] = pixel2
            pix[y2,x] = pixel1

    for i in range (0,size[0]):
        y=i
        for j in range(0,size[1],k):
            x1=j
            x2=(j+k*(key_array[k%(key_length)])**key_length)%size[1]
            pixel1 = pix[y,x1]
            pixel2 = pix[y,x2]
            pix[y,x1] = pixel2
            pix[y,x2] = pixel1