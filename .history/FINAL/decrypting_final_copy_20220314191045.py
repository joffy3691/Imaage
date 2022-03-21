import binascii
import hashlib
import json
import os
import time

import cv2
import cvlib as cv
import matplotlib.pyplot as plt
import numpy
import pandas as pd
import piexif
import piexif.helper
from backports.pbkdf2 import pbkdf2_hmac
from PIL import Image


def rotateRowRight(arr, d, n, i):
    arr[i][:] = arr[i][d:n] + arr[i][0:d]


def rotateRowLeft(arr, d, n, i):
    arr[i][:] = arr[i][n - d:n] + arr[i][0:n - d]


def rotateColDown(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[d:n, j], arr[0:d, j]))


def rotateColUp(arr, d, n, j):
    arr[:, j] = numpy.concatenate((arr[n - d:n, j], arr[0:n - d, j]))

def partialdecrypt(image, key, rsa_key, public_key,imagelocation):
    my_img = Image.open(image)
    pix = my_img.load()
    size = my_img.size
    mod = min(size)
    row, col = my_img.size[0], my_img.size[1]

    #PBKDF2
    enc_key = key
    salt = binascii.unhexlify('aaef2d3f4d77ac66e9c5a6c3d8f921d1')
    passwd = enc_key.encode("utf8")
    key = pbkdf2_hmac("sha256", passwd, salt, 50, 2048)
    # print("Derived key:", binascii.hexlify(key))
    key = binascii.hexlify(key)
    key = str(key, 'UTF-8')
    # print(key)
    key_length = len(key)
    key_array = []
    key_arra = []
    for key in key:
        key_arra.append(ord(key) % mod)
    for i in range(len(key_arra) - 5):
        # adding the alternate numbers
        sum = key_arra[i] + key_arra[i + 1] + key_arra[i + 2] + key_arra[i + 3] + key_arra[i + 4] + key_arra[i + 5]
        key_array.append(sum % mod)
    res = []
    for i in key_array:
        if i not in res:
            res.append(i)
    # print(key_array)

    
    """for i in range(len(array)):
        for j in range(col):
            print(array[i][j])"""

    #RSA
    rsa_map={}
    counter = 0
    for i in range(len(key_array)):
        
        if counter >= 256:
            break
        
        special_key=key_array[i]*key_array[i+1]
        
        if special_key not in rsa_map:
            rsa_map[special_key] = counter
            counter += 1
    # print("rsa map length = ",len(rsa_map))
    # print(rsa_map)
    data = pd.read_parquet(f'{imagelocation}.parquet.gzip')
    array = data.to_numpy()
    array1=array[0:86]
    array1=array1.flatten()
    array1=array1[:-2].tolist()
    array=array[86:]
    array = array.reshape(row, col, 3)
    D = rsa_key
    N = public_key
    # print("D decryption = ", D)
    rsa_keys1 =array1
    rsa_key_position1 = {}

    for i in range(256):
        rsa_key_position1[i] = rsa_keys1[i]

    rsa_hashing1 = {}
    for i in range(256):
        C1 = pow(rsa_keys1[i], D, N)
        rsa_hashing1[rsa_keys1[i]] = int(rsa_map[C1])

    counter=0
    rgb = set()
    for i in range(row):
        for j in range(col):
            r, g, b = array[i][j]
            M1 = rsa_hashing1.get(rsa_key_position1.get(r))
            M2 = rsa_hashing1.get(rsa_key_position1.get(g))
            M3 = rsa_hashing1.get(rsa_key_position1.get(b))
            pix[i, j] = (M1 % 256, M2 % 256, M3 % 256)
        # plt.imshow(my_img)
        # plt.show()

    

    #SCRAMBLING
    enc = [[0 for x in range(col)] for y in range(row)]
    for i in range(size[0]):
        for j in range(size[1]):
            enc[i][j] = [pix[i, j][0], pix[i, j][1], pix[i, j][2]]
    for i in range(2):
        enc = numpy.array(enc)
        for q in range(size[1] - 1, -1, -1):
            var = key_array[q] % 2
            if var:
                rotateColDown(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)
            else:
                rotateColUp(enc, (key_array[q % len(key_array)] ** 2) % size[0], size[0], q)

        enc = enc.tolist()
        for q in range(size[0] - 1, -1, -1):
            var = key_array[q] % 2
            if var:
                rotateRowRight(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)
            else:
                rotateRowLeft(enc, (key_array[q % len(key_array)] ** 2) % size[1], size[1], q)

    for i in range(size[0]):
        for j in range(size[1]):
            pix[i, j] = (enc[i][j][0], enc[i][j][1], enc[i][j][2])

    # plt.imshow(my_img)
    # plt.show()

    #CBC
    total_size=col*row
    all_pixels=[]
    random_ordering=[]
    for i in range(0,total_size):
        all_pixels.append(i)

    for i in range(0, total_size):
        pos=key_array[i%len(key_array)] ** 3 %(len(all_pixels))
        random_ordering.append(all_pixels[pos])
        # print(random_ordering[i])
        all_pixels.pop(pos)

    print(len(random_ordering)," ",total_size)
    print(random_ordering)

    for i in range(total_size-1,-1,-1):
        if(i==0):
            pos = random_ordering[0]
            q = int(pos / size[0])
            r = pos % size[1]
            reds = pix[q, r][0] ^ (key_array[0] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[0] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[0] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)

        else:
            pos=random_ordering[i]
            prev_pos=random_ordering[i-1]
            q=int(pos/row)
            r=pos%col
            randomrow=int(prev_pos/size[0])
            randomcol=prev_pos%size[1]
            # print(str(q)+" "+str(r)+" "+str(randomcol)+" "+str(randomcol))
            reds = pix[q, r][0] ^ pix[randomrow, randomcol][0]
            greens = pix[q, r][1] ^ pix[randomrow, randomcol][1]
            blues = pix[q, r][2] ^ pix[randomrow, randomcol][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
    plt.imshow(my_img)
    plt.show()
    # plt.imshow(my_img)
    # plt.show()

    my_img.save("dec_new_image.jpg")
def decryption(imagelocation,key, rsa_key, public_key):
    im = cv2.imread(imagelocation)
    data = pd.read_parquet(f'{imagelocation}.parquet.gzip')
    array = data.to_numpy()
    x1 = array[0:2]
    x1 = x1.flatten()
    x1 = x1[:-2].tolist()
    # print(x1)
    crop = im[x1[1]:x1[3], x1[0]:x1[2]]
    cv2.imwrite("crop_{1}.png", crop)
    partialdecrypt('crop_{1}.png',key, rsa_key, public_key,imagelocation)
    temp = cv2.imread("crop_{1}.png")
    im[int(x1[1]):int(x1[3]), int(x1[0]):int(x1[2])] = temp
    # plt.imshow(im)
    # plt.show()
    cv2.imwrite(imagelocation, im)
    #print("decryption over")

loc="enc_new_final_image.jpg"
tic = time.perf_counter()
partialdecrypt(loc, "ABCD", 123457466821, 802475330249,loc)
toc = time.perf_counter()
print(f"Finished encryption in {toc - tic:0.4f} seconds")
