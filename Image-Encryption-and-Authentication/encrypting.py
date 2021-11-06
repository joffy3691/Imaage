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
import random
import cv2
import cvlib as cv
import RSA
# my_img = Image.open('/home/pratyush/Downloads/Imaage-main/Experiment/PROFILE.jpeg')
# cv2_imshow(my_img)
# plt.imshow(my_img)
# pix = my_img.load()
enc = [[0 for x in range(3000)] for y in range(3000)]


def partialencrypt(image, key, column,imagelocation):
    my_img = Image.open(image)
    pix = my_img.load()
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
    res = []
    # for i in key_array:
    #    if i not in res:
    #        res.append(i)

    for q in range(size[0]):
        for r in range(size[1]):
            i = 1
            reds = pix[q, r][0] ^ pix[(q - i) % size[0], (r - i) % size[1]][0]
            greens = pix[q, r][1] ^ pix[(q - i) % size[0], (r - i) % size[1]][1]
            blues = pix[q, r][2] ^ pix[(q - i) % size[0], (r - i) % size[1]][2]
            pix[q, r] = (reds, greens, blues)
            reds = pix[q, r][0] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            greens = pix[q, r][1] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            blues = pix[q, r][2] ^ (key_array[q * r % len(key_array)] ** 2 % 255)
            pix[q, r] = (reds, greens, blues)
    plt.imshow(my_img)
    plt.show()
    E,D,N=RSA.gen_RSA_keys()
    rsa_hashing = {}
    rsa_keys = []
    for i in range(256):
        C1 = pow(i, E, N)
        rsa_hashing[i] = C1
        rsa_keys.append(C1)

    random.shuffle(rsa_keys)

    rsa_key_position = {}

    for i in range(256):
        rsa_key_position[rsa_keys[i]] = i

    # Step 5: Encryption
    size = my_img.size
    userdata = ""
    for i in range(85):
        C1 = rsa_keys[i * 3]
        C2 = rsa_keys[i * 3 + 1]
        C3 = rsa_keys[i * 3 + 2]
        column.append((C1, C2, C3))
    C1 = rsa_keys[255]
    column.append((C1, 0, 0))
    for i in range(row):
        for j in range(col):
            r, g, b = pix[i, j]
            C1 = rsa_key_position.get(rsa_hashing.get(r))
            C2 = rsa_key_position.get(rsa_hashing.get(g))
            C3 = rsa_key_position.get(rsa_hashing.get(b))
            # C1 = pow(r, E, N)
            # C2 = pow(g, E, N)
            # C3 = pow(b, E, N)
            enc[i][j] = [C1, C2, C3]
            column.append((C1, C2, C3))
            # userdata=userdata+str(C1)+","+str(C2)+","+str(C3)+","
            C1 = C1 % 256
            C2 = C2 % 256
            C3 = C3 % 256
            pix[i, j] = (C1, C2, C3)

    plt.imshow(my_img)
    plt.show()

    df = pd.DataFrame(column, columns=['C1', 'C2', 'C3'])
    df.to_parquet(f'{imagelocation}.parquet.gzip', compression='gzip')

    my_img.save(image)

    print("Encryption completed")


def encryption(imagelocation, key):
    im = cv2.imread(imagelocation)
    faces, confidences = cv.detect_face(im)
    # loop through detected faces and add bounding box
    userdata = ""
    for face in faces:
        (startX, startY) = face[0], face[1]
        (endX, endY) = face[2], face[3]
        userdata = str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3])
        column = []
        column.append((face[0], face[1], face[2]))
        column.append((face[3], 0, 0))
        crop = im[startY:endY, startX:endX]
        cv2.imwrite("crop_{0}.jpeg", crop)
        partialencrypt("crop_{0}.jpeg", key, column,imagelocation)
        cdfg = cv2.imread("crop_{0}.jpeg")
        im[startY:endY, startX:endX] = cdfg
        cv2.imwrite(imagelocation, im)