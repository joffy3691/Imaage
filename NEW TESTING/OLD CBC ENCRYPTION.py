import os, binascii
import time

from backports.pbkdf2 import pbkdf2_hmac
import matplotlib.pyplot as plt
from PIL import Image
import hashlib

def CBC_enc(imageloc,key,outputloc):
    my_img = Image.open(imageloc)
    # plt.imshow(my_img)
    pix = my_img.load()
    row, col = my_img.size[0], my_img.size[1]


    size = my_img.size
    mod = min(size)
    # print(mod)
    enc_key = key
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
    # print("Derived key:", binascii.hexlify(key))
    key=binascii.hexlify(key)
    key=str(key, 'UTF-8')
    # print(key);
    key_length = len(key)
    key_array = []
    key_sum = sum(key_array)
    key_arra = []
    for key in key:
        key_array.append(ord(key) % mod)
    res = []
    i =1
    for q in range(size[0]):
        for r in range(size[1]):
            reds = pix[q, r][0] ^ pix[(q - i) % size[0], (r - i) % size[1]][0]
            greens = pix[q, r][1] ^ pix[(q - i) % size[0], (r - i) % size[1]][1]
            blues = pix[q, r][2] ^ pix[(q - i) % size[0], (r - i) % size[1]][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q*r%len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
    # plt.imshow(my_img)
    # plt.show()
    my_img.save(f'{outputloc}.tiff')

outputloc="CBC-tiff-Enc-4.2.06"
key="ABCD"
tic = time.perf_counter()
CBC_enc("C:/Users/vishn/PycharmProjects/imo/dtjdtg/Test_images/tiff/4.2.06.tiff",key,outputloc)
toc = time.perf_counter()
print(f"Finished encryption in {toc - tic:0.4f} seconds")