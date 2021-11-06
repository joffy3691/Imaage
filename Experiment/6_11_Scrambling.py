from ctypes import sizeof
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

def rotateRowRight(arr,d,n,i):
    arr[i,:][0] = arr[i,d:n][0] + arr[i,0:d][0]


def rotateRowLeft(arr,d,n,i):
    arr[i,:][0] = arr[i,d:n][0] + arr[i,0:d][0]


def rotateColDown(arr,d,n,j):
    arr[:,j]=arr[d:n,j]+arr[0:d,j]
  

def rotateColUp(arr, d, n, j):
    arr[:,j] = arr[d:n,j] + arr[0:d,j]


my_img = Image.open('/home/pratyush/Downloads/Imaage/Image-Encryption-and-Authentication/whatsapp-1984584_960_720.png')
key = input()
pix = my_img.load()
plt.imshow(my_img)
plt.show()
size = my_img.size
row, col = my_img.size[0], my_img.size[1]
mod = min(size)
enc_key = key
salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
passwd = enc_key.encode("utf8")
key = pbkdf2_hmac("sha256", passwd, salt, 50000, 2048)
print("Derived key:", binascii.hexlify(key))
key = binascii.hexlify(key)
key = str(key, 'UTF-8')
print(key)
key_length = len(key)
key_array = []
# key_sum = sum(key_array)
key_arra = []
for key in key:
    key_arra.append(ord(key) % mod)
for i in range(len(key_arra) - 5):
    # adding the alternate numbers
    sum = key_arra[i] + key_arra[i + 1] + key_arra[i + 2] + key_arra[i + 3] + key_arra[i + 4] + key_arra[i + 5]
    key_array.append(sum % mod)
print(key_array)

#for q in range(size[0]):
#    for r in range(size[1]):
#        reds=pix[q,r][0]^(key_array[q*r%key_length]**2%255)
#        greens=pix[q,r][1]^(key_array[q*r%key_length]**2%255)
#        blues=pix[q,r][2]^(key_array[q*r%key_length]**2%255)
#        pix[q,r] = (reds,greens,blues)

for q in range(size[0]):
    for r in range(size[1]):
        reds = pix[q, r][0]
        greens = pix[q, r][1]
        blues = pix[q, r][2]
        reds1 = pix[q, (key_array[q*r%len(key_array)] ** 2)%size[1]][0]
        greens1 = pix[q, (key_array[q*r%len(key_array)] ** 2)%size[1]][1]
        blues1 = pix[q, (key_array[q*r%len(key_array)]**2)%size[1]][2]
        pix[q, (key_array[q * r % len(key_array)] ** 2) % size[1]]=(reds,greens,blues)
        pix[q, r]=(reds1,greens1,blues1)
    
    var = key_array[q] % 2
    print(size[0])
    if var:
        rotateRowLeft(pix, 5, size[0], q)
    else:
        rotateRowRight(pix, 5, size[0], q)


# for q in range(size[0]):
#     for r in range(size[1]):
#         reds = pix[q, r][0]
#         greens = pix[q, r][1]
#         blues = pix[q, r][2]
#         reds1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0], r][0]
#         greens1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0], r][1]
#         blues1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0],r][2]
#         pix[(key_array[q*r%len(key_array)] ** 2)%size[0],r]=(reds,greens,blues)
#         pix[q, r]=(reds1,greens1,blues1)

# for q in range(size[0]):
#     for r in range(size[1]):
#         reds = pix[q, r][0]
#         greens = pix[q, r][1]
#         blues = pix[q, r][2]
#         reds1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0],  (key_array[q * r % len(key_array)] ** 2) % size[1]][0]
#         greens1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0],  (key_array[q * r % len(key_array)] ** 2) % size[1]][1]
#         blues1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[0], (key_array[q * r % len(key_array)] ** 2) % size[1]][2]
#         pix[(key_array[q*r%len(key_array)] ** 2)%size[0], (key_array[q * r % len(key_array)] ** 2) % size[1]]=(reds,greens,blues)
#         pix[q, r]=(reds1,greens1,blues1)

# for q in range(size[0]):
#     for r in range(size[1]):
#         reds = pix[q, r][0]
#         greens = pix[q, r][1]
#         blues = pix[q, r][2]
#         reds1 = pix[(key_array[q*r%len(key_array)] ** 2)%size[1], r][0]
#         greens1 = pix[(key_array[q*r%len(key_array)] ** 3)%size[1], r][1]
#         blues1 = pix[(key_array[q*r%len(key_array)])%size[1], r][2]
#         pix[(key_array[q * r % len(key_array)] ** 2) % size[1], r]=(reds,pix[(key_array[q * r % len(key_array)] ** 2) % size[1], r][1],pix[(key_array[q * r % len(key_array)] ** 2) % size[1], r][2])
#         pix[(key_array[q*r%len(key_array)] ** 3)%size[1], r]=(pix[(key_array[q*r%len(key_array)] ** 3)%size[1], r][0],pix[(key_array[q*r%len(key_array)] ** 3)%size[1], r][1],blues)
#         pix[(key_array[q*r%len(key_array)])%size[1], r]=(pix[(key_array[q*r%len(key_array)])%size[1], r][0],greens,pix[(key_array[q*r%len(key_array)])%size[1], r][2])
#         pix[q, r]=(reds1,greens1,blues1)


plt.imshow(my_img)
plt.show()
my_img.save('output.jpeg') # Save the modified pixels as .png